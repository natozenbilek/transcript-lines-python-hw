# Ödev 4 kontrolü: odev4.py'yi çalıştırır, her görevin çıktısını beklenen çıktıyla karşılaştırır.
# PyCharm'da bu dosyayı açıp Run deyin. odev4.py ile aynı klasörde olmalı. Not vermez, yol gösterir.
# Görev 4'ün sorduğu puanları (seksen, 120, 80) kontrol kendisi yazar, sizin bir şey yazmanız gerekmez.
import io
import json
import os
import pathlib
import re
import subprocess
import sys
import tokenize

HERE = pathlib.Path(__file__).resolve().parent
ODEV = HERE / "odev4.py"
ANSWERS = ["seksen", "120", "80"]
MARK = "@@kontrol4@@"

EXPECTED = {
    "1. Puan listesi": ["[30, 45, 65, 70, 85, 90]", "En düşük: 30, en yüksek: 90",
                        "Ortalama: 64.17", "50 ve üstü: 4"],
    "2. Transkript satırları": ["('MAT123', 4, 'C1')", "MAT123: 4 kredi, C1", "FIZ127: 3 kredi, B2",
                                "TKD103: 2 kredi, A2", "Toplam kredi: 9"],
    "3. Haftalık ders listesi": ["['MAT123', 'FIZ127']", "['FIZ127', 'BBM101']", "False False"],
    "4. Puanı yeniden sor": ["Puan (0-100): seksen", "Tam sayı girin.", "Puan (0-100): 120",
                             "0 ile 100 arasında olmalı.", "Puan (0-100): 80", "Puan: 80"],
    "5. İlk function'lar": ["5.0", "13.0", "3.25 geçti", "1.5 kaldı"],
    "6. Sezar şifresi": ["0 28 -1", "nfsıbcb", "aös", "ödevi bitirdiniz, tebrikler"],
}
OPTIONAL = {"Meraklısına": ["Toplam atış: 600", "Hiç gelmeyen yüz var mı? False"]}

# Function'ları dosyadaki test satırlarından başka value'larla da deneriz:
# (görev, function, argument'lar, beklenen return value)
CALLS = [
    ("5.", "hypotenuse", (6, 8), 10.0),
    ("5.", "hypotenuse", (8, 15), 17.0),
    ("5.", "has_passed", (1.75,), True),
    ("5.", "has_passed", (1.7,), False),
    ("6.", "position", ("ç",), 3),
    ("6.", "position", ("A",), -1),
    ("6.", "caesar", ("çay", 2), "eca"),
    ("6.", "caesar", ("abc", -1), "zab"),
    ("6.", "caesar", ("a b!", 1), "b c!"),
]

# odev4.py'yi çalıştıran küçük program. input()'a ANSWERS'tan cevap verir ve cevabı,
# Run penceresindeki gibi, sorunun yanına yazar. Sonra CALLS'taki call'ları yapar.
RUNNER = """
import builtins, contextlib, io, json, os, sys

path, mark, calls, answers = sys.argv[1], sys.argv[2], json.loads(sys.argv[3]), sys.argv[4:]


def stop(code, reason):
    sys.stdout.flush()
    sys.stderr.write(mark + reason + chr(10))
    sys.stderr.flush()
    os._exit(code)


class Limited:
    def __init__(self, out):
        self.out, self.size = out, 0

    def write(self, text):
        self.size += len(text)
        if self.size > 100000:
            stop(4, 'cok-cikti')
        return self.out.write(text)

    def __getattr__(self, name):
        return getattr(self.out, name)


def typed_input(prompt=''):
    if not answers:
        stop(3, 'girdi-bitti')
    answer = answers.pop(0)
    print(str(prompt) + answer)
    return answer


real_out = sys.stdout
sys.stdout = Limited(sys.stdout)
builtins.input = typed_input
sys.argv = [path]
names = {'__name__': '__main__', '__file__': path, '__builtins__': builtins}
with open(path, 'rb') as f:
    code = compile(f.read(), path, 'exec')
exec(code, names)

results = []
for name, args in calls:
    func = names.get(name)
    if not callable(func):
        results.append({'yok': True})
        continue
    shown = io.StringIO()
    try:
        with contextlib.redirect_stdout(shown):
            value = func(*args)
        results.append({'deger': repr(value), 'print': shown.getvalue()})
    except Exception as e:
        results.append({'hata': type(e).__name__ + ': ' + str(e), 'print': shown.getvalue()})
sys.stdout.flush()
real_out.write(chr(10) + mark + json.dumps(results) + chr(10))
real_out.flush()
"""

HEADER = re.compile(r"""print\(\s*["']=== (.+?) ===["']\s*\)""")


def sections(text):
    """'=== başlık ===' satırlarına göre çıktıyı böler."""
    out, cur = {}, None
    for line in text.splitlines():
        m = re.fullmatch(r"=== (.+) ===", line.strip())
        if m:
            cur = m.group(1)
            out[cur] = []
        elif cur is not None:
            out[cur].append(line.rstrip())
    return out


def parse_source(src):
    """odev4.py'yi görev başlıklarına göre böler: her parça için kod satırları ve comment'ler.
    İlk başlıktan önceki kısım (import'lar) "üst" adını alır."""
    comment_at = {}
    try:
        for tok in tokenize.generate_tokens(io.StringIO(src).readline):
            if tok.type == tokenize.COMMENT:
                comment_at[tok.start[0]] = (tok.start[1], tok.string)
    except (tokenize.TokenError, SyntaxError):
        pass
    parts = {"üst": {"code": [], "comments": []}}
    cur = "üst"
    for no, line in enumerate(src.splitlines(), 1):
        code = line
        if no in comment_at:
            col, text = comment_at[no]
            code = line[:col]
            parts[cur]["comments"].append(text.lstrip("#").strip())
        m = HEADER.fullmatch(code.strip())
        if m:
            cur = m.group(1)
            parts[cur] = {"code": [], "comments": []}
        elif code.strip():
            parts[cur]["code"].append(code.rstrip())
    return parts


def func_body(lines, name):
    """def name(...): satırının altındaki, ondan daha içeride duran kod satırları."""
    out, inside, indent = [], False, 0
    for ln in lines:
        ind = len(ln) - len(ln.lstrip())
        if inside and ind > indent:
            out.append(ln)
            continue
        inside = False
        if re.match(rf"\s*def\s+{name}\s*\(", ln):
            inside, indent = True, ind
    return "\n".join(out)


def call_text(name, args):
    return f"{name}({', '.join(repr(a) for a in args)})"


# Görev 3'te dosyada hazır gelen comment'ler; bunların dışındaki bir comment açıklamanız sayılır.
GIVEN_3 = {
    "Aşağıdaki kod gelecek haftanın listesini bu haftanınkinden kurmak istiyor,",
    "ama şu haliyle this_week de değişiyor. Önce çalıştırıp çıktıya bakın.",
    "a) Neden böyle olduğunu kodun altına bir comment ile yazın.",
    "b) Tek bir satırı değiştirerek next_week'i ayrı bir list yapın.",
    "Beklenen çıktı (düzeltince):",
    "['MAT123', 'FIZ127']",
    "['FIZ127', 'BBM101']",
    "False False",
    "",
}


def source_notes(num, part, all_code, top_code):
    """Görevin .py'de yazan kurallarına bakar."""
    code = "\n".join(part["code"])
    notes = []
    if num == "1.":
        if not re.search(r"scores\.append\(\s*65\s*\)", code):
            notes.append("65'i scores.append(65) ile ekleyin")
        if not re.search(r"scores\.sort\(\s*\)", code):
            notes.append("list'i scores.sort() ile sıralayın")
        if re.search(r"\b(min|max|sorted)\(", code):
            notes.append("en düşük ve en yüksek puanı min(), max() ya da sorted() ile değil, "
                         "sıralı list'ten index ile alın")
        if "sum(" not in code or "len(" not in code:
            notes.append("ortalamayı sum() ve len() ile hesaplayın")
        if not re.search(r"\bfor\b", code):
            notes.append("50 ve üstü puanları bir for ile sayın")
        if "64.17" in code or "[30, 45" in code:
            notes.append("sonuçları kendiniz yazmayın, kod hesaplasın")
    if num == "2.":
        if not re.search(r"""\.split\(\s*["'];["']\s*\)""", code):
            notes.append('satırları split(";") ile parçalayın')
        if "int(" not in code:
            notes.append("krediyi int() ile çevirin")
        if not re.search(r"transcript\.append\(", code):
            notes.append("tuple'ları transcript.append() ile ekleyin")
        if not re.search(r"for\s+\w+\s*,\s*\w+\s*,\s*\w+\s+in\s+transcript\s*:", code):
            notes.append("dersleri for code, credits, letter in transcript: satırıyla dolaşın")
        if re.search(r"Toplam kredi:?\s*9", code):
            notes.append("toplam krediyi kendiniz yazmayın, loop'ta toplayın")
    if num == "3.":
        rhs = [m.group(1).strip() for m in re.finditer(r"(?m)^\s*next_week\s*=\s*(.+)$", code)]
        if not rhs:
            notes.append("next_week = ... satırını silmeyin, değiştirin")
        elif rhs[0] == "this_week":
            notes.append("next_week = this_week satırı hala aynı list'e ikinci bir isim veriyor")
        elif "this_week" not in rhs[0]:
            notes.append("next_week'i this_week'ten kurun, list'i elle yazmayın")
        own = [c for c in part["comments"] if c not in GIVEN_3 and "TODO" not in c]
        if not own:
            notes.append("nedenini kodun altına bir comment olarak yazın "
                         "(# TODO: açıklamanız satırının yerine)")
    if num == "4.":
        need = [("while True", r"\bwhile\s+True\b"), ("try", r"\btry\s*:"),
                ("except ValueError", r"\bexcept\s+\(?\s*ValueError\b"),
                ("continue", r"\bcontinue\b"), ("break", r"\bbreak\b")]
        missing = [name for name, pat in need if not re.search(pat, code)]
        if missing:
            notes.append("görevde istenenlerden şunlar kodda yok: " + ", ".join(missing))
    if num == "5.":
        imports = "\n".join(all_code)
        if not re.search(r"(?m)^import\s+math\b", imports):
            notes.append("import math satırı yok")
        elif not re.search(r"(?m)^import\s+math\b", "\n".join(top_code)):
            notes.append("import math'i dosyanın en üstüne, import'ların TODO'sunun yerine yazın")
        body = func_body(all_code, "hypotenuse")
        if body and "math.sqrt(" not in body:
            notes.append("hypotenuse() karekökü math.sqrt() ile hesaplasın")
    if num == "6.":
        body = func_body(all_code, "position")
        if body and not re.search(r"range\(\s*len\(\s*alphabet\s*\)\s*\)", body):
            notes.append("position() index'leri for ve range(len(alphabet)) ile dolaşsın")
        body = func_body(all_code, "caesar")
        if body:
            if not re.search(r"range\(\s*len\(\s*text\s*\)\s*\)", body):
                notes.append("caesar() text'i for ve range(len(text)) ile dolaşsın")
            if "position(" not in body:
                notes.append("caesar() her karakter için position()'ı çağırsın")
            if "%" not in body:
                notes.append("z'den sonra yeniden a gelmesi için % len(alphabet) kullanın")
    return notes


def call_notes(num, results):
    """Function'ları test satırlarındakinden başka value'larla dener."""
    notes, missing, failed = [], [], set()
    for (task, name, args, want), res in zip(CALLS, results):
        if task != num or name in failed:
            continue
        if res.get("yok"):
            if name not in missing:
                missing.append(name)
            continue
        if "hata" in res:
            notes.append(f"{call_text(name, args)} çağrısı hata verdi: {res['hata']}")
            failed.add(name)
            continue
        if name == "has_passed" and res["print"]:
            notes.append("has_passed() içinde print() olmasın, sonucu yalnızca return etsin")
            failed.add(name)
            continue
        if res["deger"] == "None" and res["print"]:
            notes.append(f"{name}() sonucu ekrana yazıyor ama return etmiyor")
            failed.add(name)
            continue
        if res["deger"] != repr(want):
            notes.append(f"{call_text(name, args)} {want!r} döndürmeli, sizinki: {res['deger']}")
            failed.add(name)
    for name in missing:
        notes.append(f"{name} adlı bir function bulunamadı")
    return notes, missing


def main():
    if not ODEV.exists():
        print("odev4.py bulunamadı. kontrol.py ile aynı klasöre koyun.")
        return
    calls = json.dumps([[name, list(args)] for _, name, args, _ in CALLS])
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    try:
        run = subprocess.run([sys.executable, "-c", RUNNER, str(ODEV), MARK, calls, *ANSWERS],
                             capture_output=True, text=True, encoding="utf-8", errors="replace",
                             timeout=15, cwd=str(HERE), env=env)
    except subprocess.TimeoutExpired:
        print("odev4.py 15 saniyede bitmedi; bir loop hiç bitmiyor olabilir.")
        print("while True'nun içinde akışın break'e ulaştığından emin olun.")
        return
    if MARK + "girdi-bitti" in run.stderr:
        print("odev4.py, Görev 4'te yazdığımız üç girdiden (seksen, 120, 80) fazlasını istedi.")
        print("80 geçerli bir puan: o gelince break ile loop'tan çıkmayı unutmuş olabilirsiniz.")
        return
    if MARK + "cok-cikti" in run.stderr:
        print("odev4.py çok fazla satır yazdı; bir loop hiç bitmiyor olabilir. Son satırlar:")
        for ln in run.stdout.splitlines()[-3:]:
            print("   ", ln)
        return
    if run.returncode != 0:
        last = [ln for ln in run.stderr.splitlines() if ln.strip()]
        where = re.findall(r'odev4\.py", line (\d+)', run.stderr)
        print("odev4.py çalışırken hata verdi. Error message'ın son satırı:")
        print("   ", last[-1] if last else "(boş)")
        if where:
            print(f"Hatanın çıktığı yer: odev4.py, {where[-1]}. satır")
        print("Önce bu hatayı düzeltin, sonra kontrolü tekrar çalıştırın.")
        return
    text, _, tail = run.stdout.partition("\n" + MARK)
    try:
        results = json.loads(tail.strip())
    except ValueError:
        results = []
    got = sections(text)
    parts = parse_source(ODEV.read_text(encoding="utf-8"))
    all_code = [ln for part in parts.values() for ln in part["code"]]
    passed = 0
    for title, want in EXPECTED.items():
        num = title.split()[0]
        have = got.get(title)
        if have is None:
            print(f"✗ {title}: başlık satırı çıktıda yok. Başlığı yazdıran print() satırını silmeyin.")
            continue
        notes = []
        if have != want:
            for i, w in enumerate(want):
                h = have[i] if i < len(have) else "(satır yok)"
                if h != w:
                    notes.append(f"{i + 1}. satır beklenen: {w!r}, sizinki: {h!r}")
                    break
            else:
                notes.append(f"beklenenden fazla satır var: {have[len(want)]!r}")
        part = parts.get(title, {"code": [], "comments": []})
        notes += source_notes(num, part, all_code, parts["üst"]["code"])
        if num in ("5.", "6.") and results:
            more, missing = call_notes(num, results)
            notes += more
            if not have and not missing:
                notes.append("test satırlarını açmayı unutmayın: seçip Ctrl+/ (macOS: Cmd+/)")
        if notes:
            print(f"✗ {title}")
            for n in notes:
                print("    " + n)
        else:
            print(f"✓ {title}")
            passed += 1
    for title, want in OPTIONAL.items():
        have = got.get(title, [])
        if have:
            it = iter(have)
            ok = all(w in it for w in want)
            print(("✓ " if ok else "· ") + title + " (zorunlu değil)")
    print(f"\n{passed} / {len(EXPECTED)} görev geçti.")


try:
    sys.stdout.reconfigure(errors="replace")
except (AttributeError, ValueError):
    pass
main()
