import reforge.api.instanceHandler, reforge.api.event, sdl2, ctypes

class EventHandler:
    def __init__(self) -> None:
        reforge.api.instanceHandler.addInstance(__name__, self)
        self._event, self.eventQueue = sdl2.SDL_Event(), []

    def pollEvents(self, eventRef: object) -> bool:
        while sdl2.SDL_PollEvent(ctypes.byref(self._event)):
            if self._event.type == sdl2.SDL_WINDOWEVENT:
                if self._event.window.event == sdl2.SDL_WINDOWEVENT_CLOSE:
                    self.eventQueue.append(reforge.api.event.Event(type = reforge.api.event.EventType.WindowClosed, windowId = self._event.window.windowID))

            elif self._event.type == sdl2.SDL_MOUSEMOTION:
                self.eventQueue.append(reforge.api.event.Event(type = reforge.api.event.EventType.MouseMotion, windowId = self._event.motion.windowID, motion = reforge.Vector2(self._event.motion.x, self._event.motion.y)))

            elif self._event.type == sdl2.SDL_MOUSEBUTTONUP:
                self.eventQueue.append(reforge.api.event.Event(type = reforge.api.event.EventType.MouseButtonUp, windowId = self._event.button.windowID, button = self._event.button.button))

            elif self._event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                self.eventQueue.append(reforge.api.event.Event(type = reforge.api.event.EventType.MouseButtonDown, windowId = self._event.button.windowID, button = self._event.button.button))

            elif self._event.type == sdl2.SDL_MOUSEWHEEL:
                self.eventQueue.append(reforge.api.event.Event(type = reforge.api.event.EventType.MouseWheel, windowId = self._event.wheel.windowID, wheel = reforge.Vector2(self._event.wheel.x, self._event.wheel.y)))

            elif self._event.type == sdl2.SDL_FINGERMOTION:
                self.eventQueue.append(reforge.api.event.Event(type = reforge.api.event.EventType.FingerMotion, windowId = self._event.tfinger.windowID, fingerId = self._event.tfinger.fingerId, motion = reforge.Vector2(self._event.tfinger.x, self._event.tfinger.y)))

            elif self._event.type == sdl2.SDL_FINGERUP:
                self.eventQueue.append(reforge.api.event.Event(type = reforge.api.event.EventType.FingerUp, windowId = self._event.tfinger.windowID, fingerId = self._event.tfinger.fingerId))

            elif self._event.type == sdl2.SDL_FINGERDOWN:
                self.eventQueue.append(reforge.api.event.Event(type = reforge.api.event.EventType.FingerDown, windowId = self._event.tfinger.windowID, fingerId = self._event.tfinger.fingerId))

            else:
                ...

        if len(self.eventQueue) > 0:
            event = self.eventQueue.pop(0)

            for i in dir(event):
                if i.startswith("_"): continue
                setattr(eventRef, i, getattr(event, i))

            return True

    def terminate(self) -> None:
        ...