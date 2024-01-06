from flask import Flask, render_template, render_template_string, request
from flask import session, redirect, url_for
import re



app = Flask(__name__)
app.secret_key = 'NisBYewndiUGWSfsd74128nd'  # Set a secret key for sessions


app.config['MAIL_SERVER'] = 'smtp.portpequa.local'
app.config['MAIL_USERNAME'] = 'sshadmin@127.0.0.1'
app.config['MAIL_PASSWORD'] = 'AIisThEFuTr3...AmIRITE?!'
app.config['API_KEY'] = '2847120jd2ni2yewuhendui267492424'

@app.route('/')
def index():
    return '''
    <link rel="stylesheet" type="text/css" href="/static/style.css">
    <header>
        <div class="container">
            <div id="branding">
                <h1><span class="highlight">PortPequa</span> Industries</h1>
            </div>
            <nav>
                <ul>
                    <li class="current"><a href="/">Home</a></li>
                    <li><a href="/employees">Employees</a></li>
                    <li><a href="/investments">Investments</a></li>
                    <li><a href="/contact">Contact</a></li>
                </ul>
            </nav>
        </div>
    </header>
    <section id="showcase">
        <div class="container">
            <h1>Welcome to the Future</h1>
            <p>Driven by AI, Fueled by Innovation</p>
        </div>
    </section>
    <footer>
        <p>&copy; 2024 PortPequa Industries, Inc.</p>
    </footer>
    '''


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Custom filter to block common SSTI payloads
        pattern = r'\{\{\s*(\d|whoami|config|bash|nc|python3?|python2\.7).*\}\}'

        if re.search(pattern, message) or re.search(pattern, name):
            return render_template('contact.html', error="Disallowed pattern detected in input.")

        # Deliberate SSTI vulnerability in hidden info
        hidden_info = f"<!-- Message received: {message} -->"
        #hidden_response = render_template_string('{{ hidden_info | safe }}', hidden_info=hidden_info
        hidden_response = render_template_string(hidden_info)
        

        # Render a thank you template with the hidden response
        return render_template('thank_you.html', hidden_response=hidden_response)
    else:
        return render_template('contact.html')


@app.route('/employees')
def employees():
    employee_data = [
        {"name": "Rick Dalton", "position": "CEO", "bio": "After inventing a time machine in his backyard shed, Rick Dalton became the CEO of PortPequa, a company specializing in retro-futuristic gadgets. Known for wearing polka-dotted suits to board meetings, Rick believes every employee should have their own pet robot. Under his leadership, the company has pioneered the development of time-traveling toasters and interdimensional coffee machines.", "image": "ceo.jpeg"},
        {"name": "Virgina Booth", "position": "CTO", "bio": "As the CTO of PortPequa, Virgina is a former astronaut who decided that exploring the stars wasn't enough; she wanted to bring space closer to Earth. Her office resembles a space station, and she's known for her star-patterned business suits and gravity-defying hairstyles. Virgina has steered her company to create the first civilian space habitat and develop educational programs that allow children to remotely control Mars rovers. Her motto: \"Reach for the stars, and if you can't reach them, build a ladder.\"", "image": "cto.jpeg"},
        {"name": "Angela Nihan", "position": "COO", "bio": "Angela, a trailblazing environmental scientist turned corporate leader, is the COO of PortPequa. Known for her eco-friendly policies and the office jungle she created (complete with a mini-waterfall), Rick champions sustainable technology. Under her leadership, the company has developed biodegradable electronics and pioneered a project to turn skyscrapers into vertical forests. Her signature accessory? A brooch made from recycled materials, symbolizing her commitment to a greener planet.", "image": "coo.jpeg"},
        {"name": "Michael Scott", "position": "CFO", "bio": "Michael, a former circus ringmaster turned tech mogul, is the visionary CFO of PortPequa. He's famous for arriving at the office riding a unicycle and conducting meetings from a treehouse. Rick's passion for mythical creatures led to the creation of the world's first holographic unicorn, now the company's mascot. His business philosophy? \"If you can dream it, you can do it, especially if it involves glitter.\"", "image": "cfo.jpeg"},
        {"name": "Phil Mickelson", "position": "CIO", "bio": "Phil, known for his outlandish theories about parallel universes, is the CIO of PortPequa. Claiming to be a time traveler from the year 3050, Rick often baffles his employees with futuristic ideas, like teleportation-based commuting and temporal email (which sends messages to the past). His office is a replica of a Victorian-era library, complete with a secret portal to other times.", "image": "cio.jpeg"},
        # Add as many employees as you like
    ]
    return render_template('employees.html', employees=employee_data)


@app.route('/investments')
def investments():
    return render_template('investments.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        
        # Check if the username is 'admin'
        if username == 'admin':
            session['username'] = username
            return redirect(url_for('index'))  # Redirect to the home page or dashboard
        else:
            return render_template('login.html', error="Invalid username")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


#appendix_b

@app.route('/appendix_b')
def appendix_2():
    return render_template('appendix_b.html')

import subprocess
import platform

@app.route('/x5ndIOmP/v2/ping', methods=['GET'])
def api_v2_ping():
    try:
        param = '-n' if platform.system().lower()=='windows' else '-c'
        # Pinging localhost once
        command = ['ping', param, '1', 'localhost']
        output = subprocess.check_output(command).decode()
        return {"status": "success", "message": "Host is active"}
    except subprocess.CalledProcessError:
        return {"status": "error", "message": "Ping failed"}, 500


if __name__ == '__main__':
    app.run(debug=True)
