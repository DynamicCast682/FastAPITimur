from GlobalSession import GlobalSession


@GlobalSession.app.get('/main2')
def main2():
  return {'message': 'Hello World2222'}