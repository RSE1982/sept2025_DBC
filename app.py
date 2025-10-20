import dash
from dash import html

app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.Iframe(
            src="assets/insurance_report.html",  # must be under assets/ to be properly served
            style={"height": "1080px", "width": "100%"},
        )
    ]
)

if __name__ == "__main__":
    app.run(debug=True)