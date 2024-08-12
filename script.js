let username = '';
let socket;

document.getElementById('setUsernameButton').addEventListener('click', function() {
    const nameInput = document.getElementById('nameInput');
    username = nameInput.value.trim();
    if (username) {
        document.getElementById('usernameModal').style.display = 'none';
        connectWebSocket();
    }
});

document.getElementById('sendButton').addEventListener('click', function() {
    const input = document.getElementById('msgInput');
    const mensagem = input.value.trim();
    if (mensagem && socket) {
        socket.send(mensagem);
        input.value = '';
    }
});

function connectWebSocket() {
    socket = new WebSocket('wss://sly-marbled-yuzu.glitch.me:15000');

    socket.onopen = function() {
        console.log("WebSocket connection established.");
        if (username) {
            socket.send(username); 
        }
    };

    socket.onmessage = function(event) {
        console.log("Mensagem recebida:", event.data);
        const areaMensagem = document.getElementById('areaMensagem');
        const newTextBox = document.createElement('div');
        newTextBox.className = 'textBox';
        newTextBox.innerText = event.data;
        areaMensagem.appendChild(newTextBox);
        areaMensagem.scrollTop = areaMensagem.scrollHeight;
    };

    socket.onerror = function(error) {
        console.error('WebSocket erro:', error);
    };

    socket.onclose = function(event) {
        console.log('WebSocket fechou:', event.reason);
    };
}

window.onload = function() {
    document.getElementById('usernameModal').style.display = 'flex';
}