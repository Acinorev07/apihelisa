from repositorio.llamadas import get

def GET(url, params):

    try:
           
       get( 
           url,
           params
        )
    
    
    
    except Exception as e:
        print(f"\nError en la ejecución: {str(e)}")
        return None