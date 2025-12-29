// 진동 기능 (햅틱 피드백)
function vibe() {
    if(navigator.vibrate) navigator.vibrate(50);
}

function sendBtn(name) {
    vibe(); // 누르면 진동
    fetch('/btn/' + name);
}

function updateVal(name, val) {
    // 숫자 업데이트
    const display = document.getElementById(name + '-val');
    if(display) display.innerText = val + '%';
    
    // 서버 전송
    fetch('/slider/' + name + '/' + val);
}