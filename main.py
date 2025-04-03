from flask import Flask, redirect, url_for, render_template,request
import ollama
import ast

app = Flask(__name__)               #creating flask class object

def ans(drug1,drug2):
    client = ollama.Client()
    prompt = """Answer **only** in tuple format. Do not provide explanations.  

Format: (drug1, drug2, severity)  

Question: given two drugs {},{} and tell about the severity of their interaction, take example of format (Aspirin, Warfarin, Severe)
  

Output:""".format(drug1,drug2)
    


    prompt2 = f"""
     Answer **only** in tuple format. Do not provide explanations. Ensure correctness., strictly follow the order

**Format:**  
(drug1_name, drug2_name, severity, details, alternatives)

**Guidelines:**  
- Use one of three severity levels: **Mild, Moderate, Severe**  
- Keep the **details concise yet informative** (1-2 sentences max).  
- If no alternatives exist, return **"None"** instead of leaving it blank.  
- Maintain proper capitalization and avoid extra characters.  

**Question:**  
What is the interaction severity between **{drug1}** and **{drug2}**?  
Follow the example format:  
(Aspirin, Warfarin, Severe, Increases risk of bleeding. Monitor INR levels closely., Acetaminophen)

**Output:**""".format(drug1,drug2)
    
    print(prompt2)
    response = client.generate("llama3.2",prompt2)
    r = response.response
    if r.startswith("(") and r.endswith(")"):
        try:
            # Remove parentheses and split manually
            tuple_response = tuple(r[1:-1].split(", "))  # Extract & convert
            print(f"Converted tuple: {tuple_response}")  # Debugging step
            return tuple_response
        except Exception as e:
            print(f"Error: {e}")
            return None
  

@app.route('/')                     #using obj function decorator
def home():
    return render_template('index.html')

@app.route('/answer/<drug1>/<drug2>')                     #using obj function decorator
def answer(drug1,drug2):
    print(drug1, drug2)
    r = ans(drug1,drug2)
    return render_template('answer.html', result = r)

@app.route('/submit',methods = ['POST','GET'])
def submit():
    if request.method == 'POST':
       d1 = request.form['drug1']
       d2 = request.form['drug2']
       return redirect(url_for("answer",drug1=d1,drug2=d2))
   

if __name__ == '__main__':          
    app.run(debug = True)           #running the flask object