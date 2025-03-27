import asyncio
from functools import wraps
import inspect
from reactivex import Observable
import reactivex.operators as op


def auto_subscribe(to_list=True):
    """
    Decorador para funciones que retornan Observables, que permite ejecutar el Observable y retornar el resultado

    :param to_list: Booleano que retona el flujo reactivo como lista si es true o como diccionario si es false, valor por defecto True
    """
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            return handle_result(result)

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return handle_result(result)

        def handle_result(result):
            if isinstance(result, Observable):
                if to_list:
                    # Ejecuta el observable y devuelve el resultado como lista
                    result_data = result.pipe(op.to_list()).run()
                    return result_data
                else:
                    # Si no se solicita como lista, simplemente retorna el Observable
                    return result.run()
            else:
                # Si no es un Observable, simplemente retorna el resultado original
                return result

        if inspect.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator
