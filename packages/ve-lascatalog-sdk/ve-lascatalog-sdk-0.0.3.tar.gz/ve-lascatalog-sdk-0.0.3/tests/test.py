from las_rest.core.client import ApiClient
from las_rest.request.catalog.api import CatalogApi
from las_rest.request.operator.api import OperatorApi

if __name__ == '__main__':
    client = ApiClient.ak_sk_mode("AKLTZDhjNGZjMzdmNTRi*", "TkRBNU9XTXdabVV3TkRJM*")
    catalogApi = CatalogApi(api_client=client, env='staging')
    operatorApi = OperatorApi(api_client=client, env='staging')
    response = catalogApi.get_catalog("hive")
    response = operatorApi.list_operators("system_catalog", "system_database", None, 1, -1)
    #  catalog_name, schema_name, operator_name, run_env, provider,
    #                         location, parameters, comment=None, tags=None, input=None, output=None
    response = operatorApi.upsert_operator("system_catalog"
                                           , "system_database"
                                           , "test_op_4"
                                           , {
                                               "Image": "volcengine/ray:latest",
                                               "Python": "/opt/conda/bin/python",
                                               "Requirements": [
                                                   "requests~=2.32.3",
                                                   "retry~=0.9.2"
                                               ]
                                           }
                                           , "字节"
                                           ,"tos://abc/aayw.db/test_op"
                                           ,parameters= [
            {
                "Name": "p1",
                "Type": "parameter",
                "Desc": "description",
                "DefaultValue": "0"
            },
            {
                "Name": "p2",
                "Type": "parameter",
                "Desc": "description",
                "DefaultValue": "0"
            },
            {
                "Name": "workers",
                "Type": "runtime",
                "Desc": "description",
                "DefaultValue": "0"
            }
        ]
                                           , comment=""
                                           , tags=[
            "Image",
            "Volc",
            "CLIP"
        ]
                                           , code_file="123"
                                           )
    response = operatorApi.get_operator("system_catalog", "system_database", "test_op_4")
    # response = operatorApi.alter_operator("testtw", "aayw", "test_op_2", comment="test_op_2")
    # response = operatorApi.list_operators("testtw", "aayw", None, 1, -1)
    # response = operatorApi.drop_operator("testtw", "aayw", "test_op_2")
    # response = operatorApi.list_operators("testtw", "aayw", None, 1, -1)

