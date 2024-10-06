# Video ref: https://www.youtube.com/watch?v=dam0GPOAvVI

from Website import create_apps

app = create_apps()

if __name__ == '__main__':
    app.run(debug=True, port=5001)