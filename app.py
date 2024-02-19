from h2o_wave import main, app, Q, ui, on, run_on
from prediction_system.prediction_function import predictor

@app('/predict')
async def serve(q: Q):
    if not q.client.initialized:
        await init(q)
        q.client.initialized = True

    await run_on(q)
    await q.page.save()

async def init(q: Q) -> None:
    q.client.cards = set()
    q.client.dark_mode = False

    q.page['header'] = ui.header_card(
        box='1 1 10 1',
        title='Sentiment Predictor Application',
        subtitle="The assignment for the h20 Wave internship",
        image='https://wave.h2o.ai/img/h2o-logo.svg'
    )

    q.page['meta'] = ui.meta_card(
        box='',
        title='Sentiment Predictor',
        theme='light',
    )

    q.page["userInput"] = ui.form_card(
        box="2 3 8 2",
        items=[
            ui.textbox(
                name="userInput_input",
                label="Input the User sentiment for prediction",
                multiline=True
            ),
            ui.buttons(
                items=[
                    ui.button(
                        name="predict",
                        label="predict",
                        primary=True,
                    )
                ]
            )
        ],
    )

    q.page['rating'] = ui.article_card(
    box='4 5 3 2',
    title='Prediction',
    content='''
The Sentiment rating prediction will be shown here!
'''
)
    
    
    q.page['footer'] = ui.footer_card(
        box='0 8 -1 1',
        caption='This sentiment predictor application was made with 💛 using [H2O Wave](https://wave.h2o.ai).'
    )

    await home(q)

@on('predict')
async def predict_review(q: Q):
    sentiment = q.args.userInput_input
    prediction = predictor.predict(sentiment)
    q.page['rating'].content = f'Prediction: {prediction}'

@on()
async def home(q: Q):
    clear_cards(q)
    add_card(q, 'form', ui.form_card(box='vertical', items=[ui.text('This is my app!')]))

def add_card(q, name, card) -> None:
    q.client.cards.add(name)
    q.page[name] = card

def clear_cards(q, ignore=[]) -> None:
    for name in q.client.cards.copy():
        if name not in ignore:
            del q.page[name]
            q.client.cards.remove(name)
