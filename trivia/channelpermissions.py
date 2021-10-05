from djangochannelsrestframework.permissions import IsAuthenticated
from typing import Dict, Any 
from channels.consumer import AsyncConsumer

'''
We may be able to get rid of this file
'''


class CustomChannel(IsAuthenticated):

    async def has_permission(
        self, scope: Dict[str, Any],
        consumer: AsyncConsumer,
            action: str,
            **kwargs
    ) -> bool:
        if action in ('list', 'retrieve'):
            return True
        return await super().has_permission(
            scope,
            consumer,
            action,
            **kwargs
        )