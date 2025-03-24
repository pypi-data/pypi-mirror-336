## API Reference for `agora-realtime-ai-api` Python Package

### `RtcOptions` Class

The `RtcOptions` class represents the configuration options for an RTC (Real-Time Communication) session.

#### Constructor:
```python
RtcOptions(
    *,
    channel_name: str = None,
    uid: int = 0,
    sample_rate: int = 24000,
    channels: int = 1,
    enable_pcm_dump: bool = False
)
```
- **channel_name**: Name of the channel.
- **uid**: Unique identifier for the user.
- **sample_rate**: Sample rate for audio (default is 24,000 Hz).
- **channels**: Number of audio channels (default is 1).
- **enable_pcm_dump**: Flag to enable PCM audio dump (default is `False`).

### `AudioStream` Class

The `AudioStream` class represents an iterable stream of PCM audio frames.

#### Constructor:
```python
AudioStream()
```

#### Methods:
- `__aiter__() -> AsyncIterator[PcmAudioFrame]`: Async iterator to traverse through audio frames.
- `__anext__() -> PcmAudioFrame`: Returns the next audio frame in the queue.

---


### `Channel` Class

The `Channel` class handles the RTC channel and associated operations such as connection, audio subscriptions, and data stream messages.

#### Constructor:
```python
Channel(rtc: "RtcEngine", options: RtcOptions)
```

#### Methods:
- `connect() -> None`: Connects to the channel asynchronously.
- `disconnect() -> None`: Disconnects from the channel asynchronously.
- `get_audio_frames(uid: int) -> AudioStream`: Returns the audio stream for a specific user.
- `push_audio_frame(frame: bytes) -> None`: Sends a PCM audio frame to the channel.
- `clear_sender_audio_buffer() -> None`: Clears the audio buffer used for sending.
- `subscribe_audio(uid: int) -> None`: Subscribes to a user's audio stream.
- `unsubscribe_audio(uid: int) -> None`: Unsubscribes from a user's audio stream.
- `send_stream_message(data: str, msg_id: str) -> None`: Sends a data stream message to the channel.

---

### `ChatMessage` Class

Represents a chat message to be sent over the RTC channel.

#### Constructor:
```python
ChatMessage(message: str, msg_id: str)
```

---

### `Chat` Class

Handles the queue of chat messages and sends them over the RTC channel.

#### Constructor:
```python
Chat(channel: Channel)
```

#### Methods:
- `send_message(item: ChatMessage) -> None`: Sends a chat message.

---

### `RtcEngine` Class

The `RtcEngine` class initializes the Agora service and provides methods for managing RTC channels.

#### Constructor:
```python
RtcEngine(appid: str, appcert: str)
```

#### Methods:
- `create_channel(options: RtcOptions) -> Channel`: Creates an RTC channel with the given options.
- `destroy() -> None`: Destroys the RTC engine instance.

---