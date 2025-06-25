from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///work_experience.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    term = db.Column(db.Integer, nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        company = request.form['company']
        term = int(request.form['term'])
        
        new_job = Job(company=company, term=term)
        db.session.add(new_job)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    jobs = Job.query.all()
    total_experience = sum(job.term for job in jobs)
    
    years = total_experience // 12
    months = total_experience % 12
    experience_str = f"{years} г. {months} мес." if years > 0 else f"{months} мес."
    
    return render_template('index.html', jobs=jobs, total_experience=experience_str)

@app.route('/delete/<int:id>')
def delete(id):
    job = Job.query.get_or_404(id)
    db.session.delete(job)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
