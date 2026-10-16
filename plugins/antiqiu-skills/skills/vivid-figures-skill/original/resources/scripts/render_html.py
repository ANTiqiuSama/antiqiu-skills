#!/usr/bin/env python
"""Render HTML with local Chrome; preserve the original geometry probe."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from resolve_runtime import resolve


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', nargs='?')
    parser.add_argument('--file', dest='source')
    parser.add_argument('--output', '--out')
    parser.add_argument('--format', choices=['pdf', 'png', 'both'], default='both')
    parser.add_argument('--width', type=int, default=1600)
    parser.add_argument('--height', type=int, default=1000)
    parser.add_argument('--render-math', action='store_true')
    parser.add_argument('--geom-check', nargs='?', const=True)
    parser.add_argument('--timeout', type=int, default=60)
    args = parser.parse_args()
    source_arg = args.input or args.source or (args.geom_check if isinstance(args.geom_check,str) else None)
    if not source_arg:
        parser.error('input HTML path required')
    source = Path(source_arg).resolve()
    if not source.is_file():
        raise SystemExit(f'HTML not found: {source}')
    chrome = resolve()['chrome']
    if not chrome:
        raise SystemExit('Chrome/Chromium not found; set CHROME_PATH')
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise SystemExit('HTML rendering requires Python playwright: python -m pip install playwright')
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=chrome, headless=True,
                                    args=['--allow-file-access-from-files'])
        page = browser.new_page(viewport={'width':args.width,'height':args.height}, device_scale_factor=2)
        page.set_default_timeout(args.timeout * 1000)
        page.goto(source.as_uri(), wait_until='load')
        if args.render_math:
            if not page.evaluate("typeof renderMathInElement === 'function'"):
                # Only formula rendering needs these pinned public assets; normal HTML is offline.
                base='https://cdn.jsdelivr.net/npm/katex@0.16.22/dist/'
                page.add_style_tag(url=base+'katex.min.css')
                page.add_script_tag(url=base+'katex.min.js')
                page.add_script_tag(url=base+'contrib/auto-render.min.js')
            page.evaluate(r'''() => renderMathInElement(document.body, {
                delimiters:[{left:'$$',right:'$$',display:true},
                            {left:'\\[',right:'\\]',display:true},
                            {left:'\\(',right:'\\)',display:false}],
                throwOnError:true,ignoredTags:['script','noscript','style','textarea','pre','code']})''')
        page.evaluate('document.fonts.ready')
        if args.geom_check:
            probe=Path(__file__).with_name('geometry-probe.js').read_text(encoding='utf-8')
            result=page.evaluate(probe)
            print(json.dumps(result,ensure_ascii=False,indent=2))
            browser.close()
            return 2 if result.get('error') else int(any(result.get(k) for k in ['overflow','clip','overlap','misalign']))
        base=Path(args.output).resolve() if args.output else source.with_suffix('')
        base.parent.mkdir(parents=True,exist_ok=True)
        target=page.locator('.fig').first if page.locator('.fig').count() else page.locator('body')
        bounds=target.bounding_box()
        if not bounds or bounds['width']<=0 or bounds['height']<=0:
            raise SystemExit('HTML has no visible figure bounds')
        outputs=[]
        if args.format in ['png','both']:
            output=base.with_suffix('.png')
            target.screenshot(path=str(output));outputs.append(output)
        if args.format in ['pdf','both']:
            output=base.with_suffix('.pdf')
            page.add_style_tag(content='@media print {html,body {margin:0!important;padding:0!important} .fig {margin:0!important;box-shadow:none!important}}')
            page.pdf(path=str(output),width=f"{bounds['width']}px",height=f"{bounds['height']}px",
                     print_background=True,margin={'top':'0','right':'0','bottom':'0','left':'0'})
            outputs.append(output)
        browser.close()
    for output in outputs:
        if not output.exists() or output.stat().st_size<256:
            raise SystemExit(f'Empty render: {output}')
        print(f'{output}\t{output.stat().st_size}')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
