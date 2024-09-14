from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prelim_grade = request.form.get('prelim_grade')

        try:
            prelim_grade = float(prelim_grade)
        except ValueError:
            return render_template('index.html', error="Please enter a valid numerical grade.")
        
        if prelim_grade < 0 or prelim_grade > 100:
            return render_template('index.html', error="Grade must be between 0 and 100.")
        
        if prelim_grade >= 75:
            return render_template('index.html', result="You have already passed!")
        
        # Calculate required midterm and final grades
        required_midterm_final = calculate_required_grades(prelim_grade)

        if required_midterm_final:
            midterm, final = required_midterm_final
            return render_template('index.html', midterm=midterm, final=final)
        else:
            return render_template('index.html', error="It's impossible to pass with the given Prelim grade.")
    
    return render_template('index.html')

def calculate_required_grades(prelim):
    overall_pass_grade = 75
    weight_prelim = 0.20
    weight_midterm = 0.30
    weight_final = 0.50

    # Calculate minimum required midterm grade
    min_midterm = (overall_pass_grade - weight_prelim * prelim) / weight_midterm

    if 0 <= min_midterm <= 100:
        # Calculate required final grade based on minimum midterm
        min_final = (overall_pass_grade - weight_prelim * prelim - weight_midterm * min_midterm) / weight_final

        if 0 <= min_final <= 100:
            return min_midterm, min_final
        
    # Return None if it's not possible to pass
    return None

if __name__ == '__main__':
    app.run(debug=True)