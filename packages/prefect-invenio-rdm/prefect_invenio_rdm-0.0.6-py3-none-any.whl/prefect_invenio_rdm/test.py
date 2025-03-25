import tasks
import flows
import asyncio

from prefect import flow


@flow
async def retrieve_requests():
    credentials = await flows.get_credentials()

    response_generator = tasks.search_user_requests(credentials=credentials, page=1, sort="newest", size=10, additional_params={
        "is_open": True,
        "shared_with_me": False,
    })

    async for response in response_generator:
        print(response)
        print("\n")

@flow
async def retrieve_records():
    credentials = await flows.get_credentials()

    response_generator = tasks.search_user_records(credentials=credentials, page=1, sort="newest", size=10, additional_params={
        "shared_with_me": False,
    })

    async for response in response_generator:
        print(response)
        print("\n")

@flow
async def accept_requests():
    credentials = await flows.get_credentials()

    result = await tasks.accept_request(credentials=credentials, request_id="b400f775-c065-43f3-b8f7-500913d540e0", payload={})
    print(result)


if __name__ == "__main__":
    # asyncio.run(retrieve_requests())

    asyncio.run(accept_requests())