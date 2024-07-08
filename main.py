<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Page</title>
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f5f5f5;
        }
        #loginBox {
            padding: 20px;
            border-radius: 10px;
            background-color: #4CAF50;
            color: #fff;
            text-align: center;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
        }
        input {
            padding: 10px;
            font-size: 16px;
            margin-bottom: 10px;
            width: 100%;
            box-sizing: border-box;
        }
        #message {
            font-size: 18px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div id="loginBox">
        <h1>Login to WiFi Router</h1>
        <input type="password" id="passwordInput" placeholder="Enter your password">
        <div id="message"></div>
    </div>
    <script>
        document.getElementById('passwordInput').addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                var userInput = document.getElementById('passwordInput').value;
                if (userInput) {
                    document.getElementById('message').innerText = "Checking password...";
                    var xhr = new XMLHttpRequest();
                    xhr.open('POST', '/check_password', true);
                    xhr.setRequestHeader('Content-Type', 'application/json');
                    xhr.onreadystatechange = function () {
                        if (xhr.readyState == 4 && xhr.status == 200) {
                            var response = JSON.parse(xhr.responseText);
                            document.getElementById('message').innerText = response.message;
                        }
                    };
                    xhr.send(JSON.stringify({ password: userInput }));
                }
            }
        });

        let docTitle = document.title;
        let intervalId; // Variable to store interval ID

        function changeTitle() {
            document.title = "Come back :D";
            setTimeout(() => {
                document.title = "PLS LOG YOURSELF";
            }, 1000); // Delay of 1000 ms (1 second) before changing the title
        }

        window.addEventListener("blur", () => {
            intervalId = setInterval(changeTitle, 2000); // Call changeTitle every 2 seconds
        });

        window.addEventListener("focus", () => {
            clearInterval(intervalId); // Clear the interval for title change
            document.title = docTitle; // Set original document title
            console.log("Welcome back!");
        });
    </script>
</body>
</html>
