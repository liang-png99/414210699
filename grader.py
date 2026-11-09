#!/usr/bin/env python3
"""任務達成評分系統：輸入前四題的結果，達標就給分（每題 20 分，滿分 100）。

用法：
  python3 grader.py                 # 讀取 results.json 並自動檢查 Git 狀態
  python3 grader.py --interactive   # 互動輸入各題結果
"""
import json
import subprocess
import sys
from pathlib import Path


def git(*args):
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    return r.returncode, r.stdout.strip()


def auto_inputs():
    res = {}
    p = Path("results.json")
    if p.exists():
        res = json.loads(p.read_text())
    code, log = git("log", "--oneline")
    commits = len(log.splitlines()) if code == 0 and log else 0
    src = Path("sum_n.f90")
    comment_lines = 0
    code_lines = 0
    if src.exists():
        for line in src.read_text().splitlines():
            if not line.strip():
                continue
            code_lines += 1
            if "!" in line:
                comment_lines += 1
    code, remote = git("remote", "-v")
    code2, ls = git("ls-remote", "--heads", "origin")
    return {
        "q1_compile_and_run": bool(res.get("compile_ok") and res.get("run_ok")),
        "q2_random_pass": int(res.get("random_pass", 0)),
        "q3_commits": commits,
        "q3_comment_ratio": (comment_lines / code_lines) if code_lines else 0.0,
        "q4_remote_set": bool(remote),
        "q4_pushed": code2 == 0 and bool(ls),
    }


def ask(prompt, cast):
    return cast(input(prompt).strip())


def interactive_inputs():
    yn = lambda s: s.lower() in ("y", "yes", "1", "true")
    return {
        "q1_compile_and_run": ask("1) 編譯並成功執行？(y/n): ", yn),
        "q2_random_pass": ask("2) 隨機驗證通過幾次 (0-3): ", int),
        "q3_commits": ask("3) Git commit 數量: ", int),
        "q3_comment_ratio": ask("3) 逐行註解比例 (0-1): ", float),
        "q4_remote_set": ask("4) 已設定 GitHub remote？(y/n): ", yn),
        "q4_pushed": ask("4) 已成功 push？(y/n): ", yn),
    }


def grade(i):
    rows = []
    rows.append(("一、編譯並成功執行", 20 if i["q1_compile_and_run"] else 0,
                 "編譯與執行皆成功" if i["q1_compile_and_run"] else "未達標"))
    rows.append(("二、三次隨機驗證", round(20 * min(i["q2_random_pass"], 3) / 3),
                 f"{min(i['q2_random_pass'], 3)}/3 次通過，全部通過才算達標"))
    s3 = 0
    if i["q3_commits"] >= 2:
        s3 += 10
    if i["q3_comment_ratio"] >= 0.8:
        s3 += 10
    rows.append(("三、Git 版本控制", s3,
                 f"commit {i['q3_commits']} 次（需 ≥2）；註解比例 {i['q3_comment_ratio']:.0%}（需 ≥80%）"))
    s4 = (10 if i["q4_remote_set"] else 0) + (10 if i["q4_pushed"] else 0)
    rows.append(("四、推送到 GitHub", s4,
                 f"remote {'已設定' if i['q4_remote_set'] else '未設定'}；push {'成功' if i['q4_pushed'] else '未成功'}"))
    return rows


def main():
    inputs = interactive_inputs() if "--interactive" in sys.argv else auto_inputs()
    rows = grade(inputs)
    total = sum(r[1] for r in rows)
    print(f"{'項目':<20}{'得分':>6}  說明")
    print("-" * 60)
    for name, score, note in rows:
        print(f"{name:<18}{score:>6}/20  {note}")
    print("-" * 60)
    print(f"{'總分':<18}{total:>6}/80（前四題）")
    print(f"第五題為本評分系統本身；折算百分制：{total / 80 * 100:.0f} 分")


if __name__ == "__main__":
    main()
