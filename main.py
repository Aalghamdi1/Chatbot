from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

# تحميل بيانات التخصصات (اسم الملف الصحيح)
df = pd.read_excel("data/specializations_KAU_fixed.xlsx")


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").strip()

    if user_input == "1":
        return jsonify({"response": "📌 شروط التقديم:\n- سعودي الجنسية\n- العمر لا يزيد عن 35 سنة\n- المعدل لا يقل عن 3.75 من 5 أو 2.75 من 4\n- 4 إلى 5 درجات في اختبار IELTS أو ما يعادلها"})

    elif user_input == "2":
        return jsonify({"response": "🎓 اكتب اسم المسار المطلوب: (صحي - علمي - اداري - ادبي)"})

    elif user_input == "3":
        return jsonify({"response": "⏰ أوقات دوام قسم إدارة البعثات:\nمن الأحد إلى الخميس\nمن الساعة 8:00 صباحًا إلى 2:00 ظهرًا"})

    elif user_input == "4":
        return jsonify({"response": "📄 لمشاهدة الأسئلة الشائعة اضغط على الرابط التالي:\nhttps://share.google/umcK9E313QXg5ohA9"})

    elif user_input in ["صحي", "علمي", "اداري", "أداري", "أدبي", "ادبي"]:
        return get_specializations(user_input)

    else:
        return jsonify({"response": "❓ الرجاء اختيار رقم من القائمة:\n1. شروط التقديم\n2. التخصصات\n3. مواعيد إدارة البعثات\n4. الأسئلة الشائعة"})

def get_specializations(category):
    category_map = {
        "صحي": "صحي",
        "علمي": "علمي",
        "اداري": "اداري",
        "أداري": "اداري",
        "أدبي": "ادبي",
        "ادبي": "ادبي"
    }

    selected_category = category_map.get(category)

    if not selected_category:
        return jsonify({"response": "⚠️ مسار غير معروف. الرجاء كتابة: صحي أو علمي أو اداري أو ادبي"})

    results = df[df['المسار'] == selected_category]

    if results.empty:
        return jsonify({"response": "❌ لا توجد تخصصات ضمن هذا المسار حالياً."})

    response = f"📚 التخصصات في المسار {selected_category}:\n\n"
    for _, row in results.iterrows():
        response += f"- {row['التخصص']}\n  الشروط: {row['الشروط']}\n  الجامعات: {row['الجامعات المتاحة']}\n\n"

    return jsonify({"response": response.strip()})

if __name__ == "__main__":
    app.run(debug=True)
