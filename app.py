from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
from groq import Groq
import os

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar o Flask
app = Flask(__name__)

# Configuração do cliente Groq
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# Lista para armazenar o histórico de interações
chat_history = []

@app.route('/', methods=['GET', 'POST'])
def chat():
    global chat_history
    if request.method == 'POST':
        # Verifica se o botão de limpar foi clicado
        if 'clear' in request.form:
            chat_history = []  # Limpa o histórico
            return redirect(url_for('chat'))  # Redireciona para a página limpa
        
        # Captura a mensagem enviada pelo usuário
        user_message = request.form['message']
        
        # Faz a requisição para a API Groq
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": user_message,
                    }
                ],
                model="llama3-8b-8192",  # Verifique se este modelo está correto para sua API
            )
            
            # Acesse o conteúdo da resposta do bot (ajuste conforme necessário)
            bot_response = chat_completion.choices[0].message.content
            
            # Adiciona a interação ao histórico
            chat_history.append({"user": user_message, "bot": bot_response})
        
        except Exception as e:
            bot_response = f"Erro ao obter resposta: {str(e)}"
            chat_history.append({"user": user_message, "bot": bot_response})
    
    # Renderiza o template passando o histórico de chat
    return render_template('chat.html', chat_history=chat_history)

if __name__ == '__main__':
    app.run(debug=True)
