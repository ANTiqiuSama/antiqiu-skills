import importlib.util
import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('monitor_policy', SKILL/'scripts/monitor_policy.py')
policy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(policy)


def shot(hour, completed=0, **changes):
    result = {'job_id':'fixture-01','observed_at':(datetime(2026,9,12,tzinfo=timezone.utc)+timedelta(hours=hour)).isoformat(),
              'status':'running','phase':'evaluation','alive':True,'identity_verified':True,
              'completed':completed,'total':100,'progress_comparable':False}
    result.update(changes)
    return result


class MonitorTests(unittest.TestCase):
    def producer_shot(self,hour,completed,total=100,seconds_per_unit=120,age=0):
        sample=shot(hour,completed,total=total,progress_comparable=True)
        now=policy.timestamp(sample['observed_at'])
        sample['progress_samples']={'job_id':sample['job_id'],'phase':sample['phase'],'total':total,
                                    'source':'fixture_completion_metadata',
                                    'points':[{'at':now-age-seconds_per_unit*(2-i),'completed':completed-2+i} for i in range(3)]}
        return sample

    def test_existing_job_history_bootstraps_eta_on_first_wakeup(self):
        _,decision=policy.observe(self.producer_shot(0,30))
        self.assertEqual(decision['eta_seconds_range'],[8400,8400])
        self.assertEqual(decision['interval_minutes'],50)
        self.assertEqual(decision['schedule_basis'],'remaining_work_eta')
        self.assertEqual(decision['eta_source'],'fixture_completion_metadata')

    def test_interval_changes_with_remaining_work_and_measured_speed(self):
        samples=[self.producer_shot(0,20,seconds_per_unit=360),
                 self.producer_shot(0,80,seconds_per_unit=360),
                 self.producer_shot(0,80,seconds_per_unit=120)]
        decisions=[policy.observe(sample)[1] for sample in samples]
        self.assertEqual([d['interval_minutes'] for d in decisions],[160,40,15])
        self.assertTrue(all(d['schedule_basis']=='remaining_work_eta' for d in decisions))

    def test_producer_clock_age_is_subtracted_and_stale_history_not_reused(self):
        _,decision=policy.observe(self.producer_shot(0,30,age=60))
        self.assertEqual(decision['eta_seconds_range'],[8340,8340])
        _,decision=policy.observe(self.producer_shot(0,30,age=600))
        self.assertIsNone(decision['eta_seconds_range'])
        self.assertEqual(decision['action'],'wait')

    def test_progress_samples_cannot_cross_identity_phase_or_current_observation(self):
        for changes in [{'job_id':'wrong'},{'phase':'other'},{'total':200}]:
            sample=self.producer_shot(0,30)
            sample['progress_samples'].update(changes)
            with self.assertRaises(ValueError): policy.observe(sample)
        sample=self.producer_shot(0,30)
        sample['progress_samples']['points'][-1]['at']+=1
        with self.assertRaises(ValueError): policy.observe(sample)

    def test_advancing_comparable_job_does_not_blindly_double_before_eta(self):
        state,_=policy.observe(shot(0,0,progress_comparable=True))
        _,decision=policy.observe(shot(1,10,progress_comparable=True),state)
        self.assertEqual(decision['interval_minutes'],60)
        self.assertEqual(decision['schedule_basis'],'collect_progress_samples')

    def test_healthy_unknown_eta_backs_off_without_false_failure(self):
        state=None
        seen=[]
        for hour in range(5):
            state, decision=policy.observe(shot(hour),state)
            seen.append(decision['interval_minutes'])
            self.assertEqual(decision['action'],'wait')
        self.assertEqual(seen,[60,120,240,240,240])

    def test_two_increments_give_phase_eta_not_one_guess(self):
        state,_=policy.observe(shot(0,0,progress_comparable=True))
        state,decision=policy.observe(shot(1,10,progress_comparable=True),state)
        self.assertIsNone(decision['eta_seconds_range'])
        state,decision=policy.observe(shot(2,20,progress_comparable=True),state)
        self.assertEqual(decision['eta_seconds_range'],[28800,28800])
        self.assertEqual(decision['interval_minutes'],160)
        state,decision=policy.observe(shot(9,90,progress_comparable=True),state)
        self.assertEqual(decision['interval_minutes'],20)

    def test_stalled_progress_invalidates_eta_without_declaring_failure(self):
        state=None
        for hour,completed in [(0,0),(1,10),(2,20)]:
            state,_=policy.observe(shot(hour,completed,progress_comparable=True),state)
        state,decision=policy.observe(shot(3,20,progress_comparable=True),state)
        self.assertIsNone(decision['eta_seconds_range'])
        self.assertEqual(decision['action'],'wait')
        state,decision=policy.observe(shot(4,30,progress_comparable=True),state)
        self.assertEqual(decision['eta_seconds_range'],[25200,50400])

    def test_phase_total_and_counter_reset_discard_old_eta(self):
        baseline=None
        for hour in range(3):
            baseline,_=policy.observe(shot(hour,hour*10,progress_comparable=True),baseline)
        for changes in [{'phase':'new'}, {'total':200}, {'completed':3}]:
            sample=shot(3,30,progress_comparable=True)
            sample.update(changes)
            state,decision=policy.observe(sample,baseline)
            self.assertIsNone(decision['eta_seconds_range'])
            self.assertEqual(len(state['history']),1)

    def test_large_variance_rejects_eta(self):
        state=None
        for hour,completed in [(0,0),(1,10),(8,20)]:
            state,decision=policy.observe(shot(hour,completed,progress_comparable=True),state)
        self.assertIsNone(decision['eta_seconds_range'])

    def test_count_full_is_not_delivery(self):
        _,decision=policy.observe(shot(0,100))
        self.assertEqual(decision['action'],'wait')
        self.assertEqual(decision['interval_minutes'],15)
        _,decision=policy.observe(shot(0,100,status='succeeded'))
        self.assertEqual(decision['action'],'escalate')

    def test_service_inactive_is_not_process_failure(self):
        _,decision=policy.observe(shot(0,service_status='inactive'))
        self.assertEqual(decision['action'],'wait')
        _,decision=policy.observe(shot(1,alive=False,identity_verified=True))
        self.assertEqual(decision['reason'],'process_missing')
        self.assertEqual(decision['action'],'escalate')

    def test_transient_unobservable_is_not_failed_job(self):
        state=None
        for hour in range(3):
            state,decision=policy.observe(shot(hour,status='unknown',identity_verified=False),state)
            self.assertEqual(decision['action'],'escalate' if hour==2 else 'wait')
        self.assertEqual(decision['reason'],'observation_unavailable')

    def test_failure_ignores_previous_long_delay(self):
        state=None
        for hour in range(3):
            state,_=policy.observe(shot(hour),state)
        state,decision=policy.observe(shot(2.1,status='failed',event_key='exit-3'),state)
        self.assertEqual(decision['action'],'escalate')
        self.assertIsNone(decision['proposed_next_check_at'])

    def test_dispatch_ack_required_and_same_worker_reused(self):
        state,decision=policy.observe(shot(0,status='failed',event_key='oom'))
        event=decision['event_id']
        with self.assertRaises(ValueError): policy.acknowledge(state,event,'handled')
        state,decision=policy.observe(shot(1,status='failed',event_key='oom'),state)
        self.assertEqual(decision['action'],'escalate')
        state=policy.acknowledge(state,event,'dispatched','actual-agent-123')
        with self.assertRaises(ValueError): policy.acknowledge(state,event,'dispatched','duplicate-agent-456')
        state,decision=policy.observe(shot(2,status='needs_decision',event_key='new-detail'),state)
        self.assertEqual(decision['action'],'wait_for_worker')
        self.assertEqual(decision['worker_id'],'actual-agent-123')
        state=policy.acknowledge(state,event,'handled')
        _,decision=policy.observe(shot(3,status='failed',event_key='oom'),state)
        self.assertEqual(decision['action'],'stop')

    def test_pending_incident_not_lost_after_recovery(self):
        state,decision=policy.observe(shot(0,status='failed',event_key='transient',detail='specific original failure'))
        state,decision=policy.observe(shot(1),state)
        self.assertEqual(decision['action'],'escalate')
        self.assertEqual(state['handoff']['status'],'pending')
        self.assertEqual(state['handoff']['trigger_snapshot']['detail'],'specific original failure')
        self.assertEqual(decision['reason'],'failed')

    def test_worker_can_release_same_job_then_rearm_after_recovery(self):
        state,decision=policy.observe(shot(0,status='needs_decision',event_key='review'))
        event=decision['event_id']
        state=policy.acknowledge(state,event,'dispatched','worker-1')
        state=policy.acknowledge(state,event,'resume')
        state,decision=policy.observe(shot(1,status='needs_decision',event_key='review'),state)
        self.assertEqual(decision['action'],'wait')
        state,decision=policy.observe(shot(2),state)
        self.assertIsNone(state['handoff'])
        state,decision=policy.observe(shot(3,status='needs_decision',event_key='review'),state)
        self.assertEqual(decision['action'],'escalate')

    def test_new_pending_detail_keeps_original_incident(self):
        state,decision=policy.observe(shot(0,status='failed',event_key='first',detail='first evidence'))
        first=decision['event_id']
        state,decision=policy.observe(shot(1,status='failed',event_key='second',detail='second evidence'),state)
        self.assertEqual(decision['event_id'],first)
        self.assertNotEqual(decision['observed_event_id'],first)
        self.assertEqual(state['handoff']['trigger_snapshot']['detail'],'first evidence')
        self.assertEqual(state['handoff']['latest_incident']['snapshot']['detail'],'second evidence')

    def test_unknown_probe_does_not_rearm_reviewed_incident(self):
        state,decision=policy.observe(shot(0,status='needs_decision',event_key='review'))
        event=decision['event_id']
        state=policy.acknowledge(state,event,'dispatched','worker-1')
        state=policy.acknowledge(state,event,'resume')
        state,decision=policy.observe(shot(1,status='unknown',identity_verified=False),state)
        self.assertEqual(state['handoff']['status'],'released')
        state,decision=policy.observe(shot(2,status='needs_decision',event_key='review'),state)
        self.assertEqual(decision['action'],'wait')

    def test_finished_monitor_stays_stopped_after_late_probe(self):
        state,decision=policy.observe(shot(0,status='succeeded'))
        event=decision['event_id']
        state=policy.acknowledge(state,event,'dispatched','worker-1')
        state=policy.acknowledge(state,event,'handled')
        for sample in [shot(1),shot(2,status='unknown'),shot(3,status='failed')]:
            state,decision=policy.observe(sample,state)
            self.assertEqual(decision['action'],'stop')
            self.assertIsNone(decision['interval_minutes'])

    def test_invalid_state_identity_and_stale_input_do_not_write(self):
        state,_=policy.observe(shot(0))
        for sample in [shot(0),shot(1,job_id='different'),shot(1,completed=101),shot(1,progress_comparable='true')]:
            with self.assertRaises((ValueError,TypeError)): policy.observe(sample,state)
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'state.json'
            policy.save_json(path,state)
            self.assertEqual(policy.load_json(path),state)
            self.assertEqual(len(list(Path(folder).iterdir())),1)


if __name__=='__main__':
    unittest.main(verbosity=2)
