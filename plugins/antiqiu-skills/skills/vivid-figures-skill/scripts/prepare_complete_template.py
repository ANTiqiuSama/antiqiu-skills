"""Copy a complete composition unchanged; its existing CLI remains the renderer."""
from pathlib import Path
import argparse
import json
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'original/resources/assets/shared-scripts'))
from template_sources import digest, materialize


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--id', required=True, choices=['template.sem_violin_pearson', 'template.shap_dependence', 'template.shap_contribution'])
    parser.add_argument('--script', required=True, type=Path)
    parser.add_argument('--workspace', type=Path)
    args = parser.parse_args()
    relative = ('templates/sem-violin-pearson/plot_sem_violin_pearson.py' if args.id == 'template.sem_violin_pearson'
                else 'templates/shap-composites/plot_shap_composites.py')
    code = (ROOT/relative).read_text(encoding='utf-8')
    source = dict(id=args.id, variant=args.id.split('.')[-1], file=relative, codeSha256=digest(code))
    print(json.dumps(materialize(args.script, code, source, args.workspace), ensure_ascii=False))


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')
    try: main()
    except (ValueError, OSError) as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
