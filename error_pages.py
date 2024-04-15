RETRY = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Discord-like Page</title>
        <style>
            html, body {
                height: 100%;
                margin: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                background-color: #36393f; /* Discord-like background color */
                color: #fff; /* Text color */
                font-family: Arial, sans-serif;
            }
            
            h1 {
                font-size: 24px;
                margin-bottom: 20px;
            }
            
            .button {
                padding: 10px 20px;
                background-color: #7289da; /* Discord-like button color */
                color: #fff;
                text-decoration: none;
                border-radius: 4px;
            }
        </style>
    </head>
    <body>
        <a href="http://localhost:5000/?auth_key=fuck" class="button">Retry</a>
    </body>
    </html>
'''
INVALID_USER = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Discord-like Page</title>
        <style>
            html, body {
                height: 100%;
                margin: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                background-color: #36393f; /* Discord-like background color */
                color: #fff; /* Text color */
                font-family: Arial, sans-serif;
            }
            
            h1 {
                font-size: 24px;
                margin-bottom: 20px;
            }
            
            .button {
                padding: 10px 20px;
                background-color: #7289da; /* Discord-like button color */
                color: #fff;
                text-decoration: none;
                border-radius: 4px;
            }
        </style>
    </head>
    <body>
        <h1>You do not have a license key!</h1>
        <a href="http://localhost:5000/?auth_key=fuck" class="button">Purchase</a>
    </body>
    </html>
'''
EXPIRED_USER = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Discord-like Page</title>
        <style>
            html, body {
                height: 100%;
                margin: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                background-color: #36393f; /* Discord-like background color */
                color: #fff; /* Text color */
                font-family: Arial, sans-serif;
            }
            
            h1 {
                font-size: 24px;
                margin-bottom: 20px;
            }
            
            .button {
                padding: 10px 20px;
                background-color: #7289da; /* Discord-like button color */
                color: #fff;
                text-decoration: none;
                border-radius: 4px;
            }
        </style>
    </head>
    <body>
        <h1>Your license key has expired!</h1>
        <!--<a href="http://localhost:5000/?auth_key=fuck" class="button">Retry</a>-->
    </body>
    </html>
'''
IN_USE = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Discord-like Page</title>
        <style>
            html, body {
                height: 100%;
                margin: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                background-color: #36393f; /* Discord-like background color */
                color: #fff; /* Text color */
                font-family: Arial, sans-serif;
            }
            
            h1 {
                font-size: 24px;
                margin-bottom: 20px;
            }
            
            .button {
                padding: 10px 20px;
                background-color: #7289da; /* Discord-like button color */
                color: #fff;
                text-decoration: none;
                border-radius: 4px;
            }
        </style>
    </head>
    <body>
        <h1>Your license key is in use!</h1>
        <!--<a href="http://localhost:5000/?auth_key=fuck" class="button">Retry</a>-->
    </body>
    </html>
'''
CANNOT_CONNECT_TO_SERVER = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Discord-like Page</title>
        <style>
            html, body {
                height: 100%;
                margin: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                background-color: #36393f; /* Discord-like background color */
                color: #fff; /* Text color */
                font-family: Arial, sans-serif;
            }
            
            h1 {
                font-size: 24px;
                margin-bottom: 20px;
            }
            
            .button {
                padding: 10px 20px;
                background-color: #7289da; /* Discord-like button color */
                color: #fff;
                text-decoration: none;
                border-radius: 4px;
            }
        </style>
    </head>
    <body>
        <h1>Cannot connect to server!</h1>
        <!--<a href="http://localhost:5000/?auth_key=fuck" class="button">Retry</a>-->
    </body>
    </html>
'''
BOT_OUTDATED = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Discord-like Page</title>
        <style>
            html, body {
                height: 100%;
                margin: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                background-color: #36393f; /* Discord-like background color */
                color: #fff; /* Text color */
                font-family: Arial, sans-serif;
            }
            
            h3 {
                font-size: 18px;
                margin-bottom: 20px;
                text-align: center; /* Ensures text is centered */
                width: 100%; /* Ensures h1 takes full width */
                margin-left: 20px; /* Adds margin to the left */
                margin-right: 20px; /* Adds margin to the right */
            }
        </style>
    </head>
    <body>
        <h3>This version of the bot is outdated, please visit discord to download the new version!</h3>
    </body
'''