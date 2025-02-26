"""Common type hints."""

import tcod.ecs

import tqueue.tqueue

TurnQueue_ = tqueue.tqueue.TurnQueue[tcod.ecs.Entity]
Ticket_ = tqueue.tqueue.Ticket[tcod.ecs.Entity]
