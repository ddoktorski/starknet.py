import os.path

import pytest

from src.contract import Contract
from src.net.account.account_client import AccountClient


directory = os.path.dirname(__file__)
map_source_fname = os.path.join(directory, "map.cairo")
map_source_code = open(map_source_fname).read()


@pytest.mark.asyncio
async def test_deploy_account_contract_and_sign_tx():
    acc_client = await AccountClient.create_account(net="http://localhost:5000/")

    map_contract = await Contract.deploy(
        client=acc_client, compilation_source=map_source_code
    )
    k, v = 13, 4324
    await map_contract.functions.put.invoke(k, v)
    resp = await map_contract.functions.get.call(k)

    assert resp["res"] == v