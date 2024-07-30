# from data.single_pred_tasks.tasks import _TASKS
import task_datasets as data
import benchmark.groups as benchmark_groups
import benchmark.leaderboards as benchmark_leaderboards

from flask import Flask, flash, redirect, render_template, request, session, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start')
def start():
    return render_template('start.html')

@app.route('/overview')
def overview():
    return render_template('overview/index.html')

@app.route('/single_pred_tasks/overview')
def single_pred_tasks():
    vars = {
        "items": data.single_pred_tasks.tasks,
        "data": [(endpt, label, data.single_pred_tasks.datasets[endpt]) for endpt, label, _ in data.single_pred_tasks.tasks[1:]] # skip adme 
    }
    return render_template('single_pred_tasks/index.html', **vars)

@app.route("/single_pred_tasks/<task>")
def single_pred_tasks_data(task):
    if task == "adme":
        return render_template("single_pred_tasks/adme.html")
    elif task in data.single_pred_tasks.datasets:
        datasets = []
        for var in data.single_pred_tasks.datasets[task]:
            if var in data.single_pred_tasks.meta:
                if len(data.single_pred_tasks.meta[var]) != 10:
                    raise Exception(var, len(data.single_pred_tasks.meta[var])) 
                datasets.append([var] + data.single_pred_tasks.meta[var])
        desc = data.single_pred_tasks.desc[task]
        args = {
            "datasets": datasets,
            "task": task,
            "desc_id": desc[0],
            "desc_title": desc[1],
            "desc_desc": desc[2],
            "desc_impact": desc[3],
            "desc_gen": desc[4],
            "desc_product": desc[5],
            "desc_pipeline": desc[6],
        }
        return render_template("single_pred_tasks/task.html", **args)
    return redirect("/single_pred_tasks/overview")

@app.route("/multi_pred_tasks/overview")
def multi_pred_tasks():
    vars = {
        "items": data.multi_pred_tasks.tasks,
        "data": [(endpt, label, data.multi_pred_tasks.datasets[endpt]) for endpt, label, _ in data.multi_pred_tasks.tasks]
    }
    return render_template("multi_pred_tasks/index.html", **vars)

@app.route("/multi_pred_tasks/<task>")
def multi_pred_task_data(task):
    if task == "catalyst":
        return render_template("multi_pred_tasks/catalyst.html")
    elif task == "ddi":
        return render_template("multi_pred_tasks/ddi.html")
    elif task == "drugres":
        return render_template("multi_pred_tasks/drugres.html")
    elif task == "dti":
        return render_template("multi_pred_tasks/dti.html")
    elif task == "mti":
        return render_template("multi_pred_tasks/mti.html")
    elif task == "ppi":
        return render_template("multi_pred_tasks/ppi.html")
    elif task == "proteinpeptide":
        return render_template("multi_pred_tasks/proteinpeptide.html")
    elif task == "tcrepitope":
        return render_template("multi_pred_tasks/tcrepitope.html")
    elif task == "antibodyaff":
        return render_template("multi_pred_tasks/antibodyaff.html")
    elif task == "trialoutcome":
        return render_template("multi_pred_tasks/trialoutcome.html")
    elif task == "scdti":
        return render_template("multi_pred_tasks/scdti.html")
    elif task == "counterfactual":
        return render_template("multi_pred_tasks/counterfactual.html")
    elif task in data.multi_pred_tasks.datasets:
        datasets = []
        for var in data.multi_pred_tasks.datasets[task]:
            if var in data.multi_pred_tasks.meta:
                if len(data.multi_pred_tasks.meta[var]) != 10:
                    raise Exception(var, len(data.multi_pred_tasks.meta[var])) 
                datasets.append([var] + data.multi_pred_tasks.meta[var])
        desc = data.multi_pred_tasks.desc[task]
        args = {
            "datasets": datasets,
            "task": task,
            "desc_id": desc[0],
            "desc_title": desc[1],
            "desc_desc": desc[2],
            "desc_impact": desc[3],
            "desc_gen": desc[4],
            "desc_product": desc[5],
            "desc_pipeline": desc[6],
        }
        return render_template("multi_pred_tasks/task.html", **args)
    else:
        return redirect("/multi_pred_tasks/overview")
        
@app.route("/generation_tasks/overview")
def generation_tasks():
    return render_template("generation_tasks/index.html")

@app.route("/generation_tasks/<task>")
def generation_tasks_data(task):
    if task == "molgen":
        return render_template("generation_tasks/molgen.html")
    elif task == "reaction":
        return render_template("generation_tasks/reaction.html")
    elif task == "retrosyn":
        return render_template("generation_tasks/retrosyn.html")
    elif task == "sbdd":
        return render_template("generation_tasks/sbdd.html")
    else:
        return redirect("/generation_tasks/overview")

@app.route("/fct_overview")
def fct_overview():
    return render_template("/fct_overview.html")

@app.route("/functions/<section>")
def function_page(section):
    if section == "oracles":
        return render_template("/functions/oracles.html")
    elif section == "data_evaluation":
        return render_template("/functions/data_evaluation.html")
    elif section == "data_process":
        return render_template("/functions/data_process.html")
    elif section == "data_split":
        return render_template("/functions/data_split.html")
    else:
        return redirect("/fct_overview")

@app.route("/benchmark")
def benchmark():
    return render_template("/benchmark/index.html")

@app.route("/benchmark/overview")
def benchmark_overview():
    return render_template("/benchmark/index.html")

@app.route("/benchmark/<group>/<leaderboard>")
def benchmark_leaderboard_overview(group, leaderboard):
    leads = benchmark_groups._GROUP_MEMBERSHIP[group]
    if leaderboard == "overview":
        group = '_'.join(group.split("_")[:-1])
        s = "/benchmark/{}.html".format(group)
        args = {
            "leaderboards": leads
        }
        return render_template(s, **args)
    else:
        lb = benchmark_leaderboards._LEADERBOARDS[leaderboard]
        order, entries, scores = lb[2], lb[3], lb[4]
        if len(entries) != len(scores):
            raise ValueError("length of lb entries {} does not match length of provided scores {} for lb {}".format(len(entries), len(scores), leaderboard))
        increasing = order == "incr"
        sidxs = sorted([i for i in range(len(entries))], key=lambda idx: entries[idx][-1] if increasing else -entries[idx][-1])
        lb[3] = [entries[i] for i in sidxs]
        lb[4] = [scores[i] for i in sidxs]
        args = {
            "entries": entries,
            "scores": scores,
            "group": group,
            "leaderboard": leaderboard,
            "style": lb[0],
            "cols": lb[1],
            "extra_vals": lb[-1],
            "extra_cols": lb[-2],
            "leaderboards": leads,
        }
        return render_template("/benchmark/leaderboard.html", **args)

    

if __name__ == '__main__':
    app.run(debug=True)  # debug=True for development mode