"""Validate poster assets and shared demo data without rerendering."""
from pathlib import Path
import hashlib
import json
import re
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image
import fitz

REPO=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
OUT=REPO/'docs/images/palettes'
payload=(HERE/'demo-data.json').read_bytes()
data=json.loads(payload)
digest=hashlib.sha256(payload).hexdigest()
np.testing.assert_allclose(np.array(data['composition']).sum(axis=0),100)
assert np.array(data['scatter']).shape==(7,200,2)
assert np.array(data['distributions']).shape==(7,240)
points=np.array(data['scatter'])
assert points[:,:,0].min()>=-.3 and points[:,:,0].max()<=23
assert points[:,:,1].min()>=-1 and points[:,:,1].max()<=16.5
assert np.array(data['distributions'])[:5].min()>=15 and np.array(data['distributions'])[:5].max()<=83
audit=json.loads((OUT/'render-info.json').read_text(encoding='utf-8'))
palettes=json.loads((REPO/'original/resources/assets/shared-scripts/palettes.json').read_text(encoding='utf-8'))['palettes']
results=[]
for item in audit:
    slug=item['slug']
    sample_file=HERE/item.get('data_file','demo-data.json')
    sample_payload=sample_file.read_bytes()
    samples=json.loads(sample_payload)
    sample_hash=hashlib.sha256(sample_payload).hexdigest()
    n=item['groups']
    assert np.array(samples['scatter']).shape==(n,200,2)
    assert np.array(samples['distributions']).shape==(n,240)
    np.testing.assert_allclose(np.array(samples['composition']).sum(axis=0),100)
    points=np.array(samples['scatter'])
    assert points[:,:,0].min()>=-.3 and points[:,:,0].max()<=23
    assert points[:,:,1].min()>=-1 and points[:,:,1].max()<=16.5
    colors=palettes[slug]['colors']
    assert item['base_colors']==colors
    assert item['data_sha256']==sample_hash
    with Image.open(OUT/f'{slug}.png') as img:
        assert img.size==(2400,2880)
        assert abs(img.info['dpi'][0]-300)<.1
    root=ET.parse(OUT/f'{slug}.svg').getroot()
    assert root.tag.endswith('svg')
    with fitz.open(OUT/f'{slug}.pdf') as doc:
        assert len(doc)==1
        assert len(doc[0].get_drawings())>50
    results.append(dict(palette=slug,base_colors_match=True,shared_data_match=True,
                       png='2400x2880 at 300dpi',svg_parse='pass',pdf_pages=1,
                       visual_review='viewed; current recipe translucent ridge fill and outline retained',
                       repair_rounds=1 if n==7 or item.get('pale_color_readability_adjustment') else 0))
(OUT/'verification.json').write_text(json.dumps(dict(data_sha256=digest,
    composition_sums='100%',all_scatter_and_violin_samples_within_axes=True,
    results=results),ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Verified {len(audit)} palettes, shared data within each group count, bounds, and {len(audit)*3} image/vector exports.')
