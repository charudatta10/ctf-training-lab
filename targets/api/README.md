# target/api - GlowMart Mobile backend

Small Flask backend the vulnerable app talks to. Serves both a plain HTTP
endpoint (`:3000`) and the pinned-TLS endpoint (`:3443`) used by the
Module 3 SSL-pinning lab.

``certs/`` contains a committed self-signed certificate/key pair:

- `server.crt` - the leaf cert the app pins to
- `server.key` - the corresponding RSA private key (PKCS#8 PEM)

The app's `PinnedApiClient` compares the server leaf's SPKI against
`PIN_SHA256 = +zSd3zPVaGL3CmRb7lO45beFNK/lw+4D+fb43RZg91Y=`
(sha256 of the SPKI DER, base64). Interception succeeds only after that
pin check is bypassed (e.g. a Frida hook on `checkServerTrusted`).

## Reachability

- Host loopback: `http://127.0.0.1:3000` and `https://127.0.0.1:3443`
- Android emulator: `http://10.0.2.2:3000` and `https://10.0.2.2:3443`
- LAN devices (when `EXPOSE_TARGETS=1`): the host's LAN IP on both ports