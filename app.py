from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'any_secret_key_for_sessions'

fake_projects = ["Project Alpha", "Project Beta", "Project Gamma"]
fake_tasks = {
    "Project Alpha": ["Task A1", "Task A2"],
    "Project Beta": ["Task B1", "Task B2"],
    "Project Gamma": ["Task C1", "Task C2"],
}

TEMPLATE_BASE = """
<!doctype html>
<title>Taiga Mini App (Python)</title>
<style>
body {{ background:#222; color:#eee; font-family:sans-serif; }}
.wrap {{
  max-width:380px; margin:50px auto; background:#292929; border-radius:16px;
  padding:32px 24px; box-shadow:0 4px 32px rgba(0,0,0,.5); text-align:center;
}}
input, button {{
  font-size:17px; border-radius:8px; border:none; margin-bottom:10px;
  padding:8px 14px;
}}
button {{ background:#3b82f6; color:white; cursor:pointer; }}
button:hover {{ background:#2563eb; }}
a {{ color:#5af; text-decoration:none; }}
form.inline {{ display:inline; }}
ul {{ text-align:left; list-style-position:inside; padding:0; }}
li {{}}
</style>
<div class="wrap">
  {body}
</div>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session['token'] = request.form.get("token")
        return redirect(url_for('projects'))
    return render_template_string(TEMPLATE_BASE.format(body="""
        <h2>Taiga Mini App (Python)</h2>
        <form method="post">
            <p>Введите API токен (фиктивно)</p>
            <input type="text" name="token" placeholder="API Token" required><br><br>
            <button type="submit">Войти</button>
        </form>
    """))

@app.route("/projects", methods=["GET", "POST"])
def projects():
    if 'token' not in session:
        return redirect(url_for('login'))
    if request.method == "POST":
        session['project'] = request.form.get("project")
        return redirect(url_for('tasks'))
    projects_html = "".join(
        f'<form method="post" style="margin-bottom:8px">'
        f'<input type="hidden" name="project" value="{proj}">'
        f'<button type="submit" style="width:100%">{proj}</button></form>'
        for proj in fake_projects
    )
    return render_template_string(TEMPLATE_BASE.format(body=f"""
        <h2>Выберите проект</h2>
        {projects_html}
        <br>
        <a href="{url_for('login')}">Выйти</a>
    """))

@app.route("/tasks", methods=["GET", "POST"])
def tasks():
    if 'project' not in session:
        return redirect(url_for('projects'))
    proj = session['project']
    tasks = fake_tasks.get(proj, [])
    if request.method == "POST":
        session['current_task'] = request.form.get("task")
        return redirect(url_for('add_time'))
    tasks_html = "".join(
        f'''<li>
                <form method="post" class="inline" style="display:inline">
                    <input type="hidden" name="task" value="{task}">
                    {task} — <button type="submit">Ввести время</button>
                </form>
            </li>'''
        for task in tasks
    )
    return render_template_string(TEMPLATE_BASE.format(body=f"""
        <h2>Проект: {proj}</h2>
        <ul>{tasks_html}</ul>
        <br>
        <a href="{url_for('projects')}">Назад к проектам</a>
    """))

@app.route("/add_time", methods=["GET", "POST"])
def add_time():
    if 'current_task' not in session:
        return redirect(url_for('tasks'))
    task = session['current_task']
    if request.method == "POST":
        # Тут можно обработать введённое время (фиктивно)
        hours = request.form.get("hours")
        minutes = request.form.get("minutes")
        # Можно добавить сохранение или что-то ещё, но тут просто "заглушка"
        session.pop('current_task', None)
        return render_template_string(TEMPLATE_BASE.format(body=f"""
            <h2>Время добавлено!</h2>
            <p>Для задачи <b>{task}</b> вы ввели: {hours} часов {minutes} минут.</p>
            <br>
            <a href="{url_for('tasks')}">Назад к задачам</a>
        """))
    return render_template_string(TEMPLATE_BASE.format(body=f"""
        <h2>Ввод времени для задачи:<br>{task}</h2>
        <form method="post">
            <input type="number" name="hours" min="0" max="24" placeholder="Часы" required> <br>
            <input type="number" name="minutes" min="0" max="59" placeholder="Минуты" required> <br>
            <button type="submit">Сохранить (заглушка)</button>
        </form>
        <br>
        <a href="{url_for('tasks')}">Назад к задачам</a>
    """))

if __name__ == "__main__":
    app.run(debug=True)
