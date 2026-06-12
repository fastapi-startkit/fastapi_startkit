"""Channel authorization callbacks.

Register authorization callbacks for private and presence channels here
using the ``@Broadcast.channel()`` decorator.  This file is auto-loaded
by ``ReverbProvider`` when it boots — no manual import required.

Usage
-----
Decorate an async function with ``@Broadcast.channel("<channel-pattern>")``.
The channel name may contain ``{wildcard}`` segments that are extracted and
injected as typed parameters into the callback.

The first positional argument receives the currently-authenticated user
(resolved from the container's ``auth`` service or ``request.state.user``).
Return ``True`` to allow subscription, ``False`` to deny.

Supported channel types:
  - ``Channel("name")``          — public, no auth required
  - ``PrivateChannel("name")``   — auth checked via @Broadcast.channel
  - ``PresenceChannel("name")``  — auth checked + member tracking

This file is auto-loaded by ``ReverbProvider`` when it boots.
"""

from fastapi_startkit.facades.Broadcast import Broadcast  # noqa: F401

# ---------------------------------------------------------------------------
# Define your channel authorization callbacks below.
# ---------------------------------------------------------------------------
#
# @Broadcast.channel("orders.{order_id}")
# async def authorize_orders_channel(user, order_id: int) -> bool:
#     """Authorize the private ``orders.{order_id}`` channel.
#
#     ``order_id`` is extracted from the channel name and coerced to ``int``
#     via the type hint.  ``user`` is the authenticated user resolved from the
#     service container.
#
#     Return ``True`` to grant access, ``False`` to deny.
#     """
#     return user is not None and user.id == order_id
