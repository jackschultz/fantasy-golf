from flask import Flask
from flask import render_template, make_response, request, url_for, redirect
from flask.ext.assets import Environment, Bundle

from models.tournament import Tournament
from models.player import Player
from models.user import User
from models.user import Pick
import mongoengine as me

me.connect('fg')

app = Flask(__name__)
app.debug=True


assets = Environment(app)

js = Bundle('vendor/jquery/jquery-2.0.3.min.js', output='gen/packed.js')
assets.register('js_all', js)

css = Bundle('vendor/bootstrap/css/bootstrap.min.css', 'css/sticky-footer.css',
            output='gen/packedcss.css')

assets.register('css_all', css)

@app.route('/')
def index():
    return render_template('index.html')

if False:
    @app.route("/login", methods=["GET", "POST"])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            login_user(user)
            return redirect(url_for("index"))
        return render_template("login.html", form=form)


@app.route('/tournaments')
def tournaments():
    tournaments = Tournament.objects.order_by('end_date')
    return render_template('tournaments.html', tournaments=tournaments)

@app.route('/tournaments/<tid>')
def tournament(tid):
    tournament = Tournament.objects.get(id=tid)
    return render_template('tournament.html', tournament=tournament)

@app.route('/tournaments/<tid>/pick', methods=["GET", "POST"])
def tournaments_pick(tid):
    tournament = Tournament.objects.get(id=tid)
    if request.method == 'POST':
        user = User.objects.get(id=request.form['user_id'])
        player = Player.objects.get(id=request.form['player_id'])
        pick = Pick(tournament=tournament, player=player)
        pick.save()
        user.update(add_to_set__picks=pick)
        user.save()
    users = User.objects
    return render_template('tournament_picks.html', tournament=tournament, users=users)

@app.route('/tournaments/<tid>/pick/delete', methods=["POST"])
def tournaments_pick_delete(tid):
    pick = Pick.objects.get(id=request.form['pid'])
    pick.delete()
    return redirect(url_for('tournaments_pick', tid=tid))



if __name__ == '__main__':
    app.run()
