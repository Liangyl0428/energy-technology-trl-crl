"""Publish only the changed taxonomy inputs; source evidence stays in data/."""
import hashlib
import json
import shutil
from pathlib import Path

REPO=Path(__file__).resolve().parents[2]


def export():
    dest=REPO/'assets/nmf500/taxonomy_overlay'
    dest.mkdir(parents=True,exist_ok=True)
    for name in ['dataset','objects','case_technology_links','themes','theme_direction_links']:
        shutil.copy2(REPO/'work/nmf500/inputs'/(name+'.json'),dest/(name+'.json'))
    manifest={str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest()
              for directory in [dest,REPO/'results/nmf500'] for p in sorted(directory.rglob('*')) if p.is_file()}
    (dest.parent/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print('Exported portable taxonomy overlay and',len(manifest),'checksums')


if __name__=='__main__':
    export()
