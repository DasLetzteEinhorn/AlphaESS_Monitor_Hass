ARG BUILD_FROM=hassioaddons/base:7.0.2
# hadolint ignore=DL3006
FROM ${BUILD_FROM}

# Copy root filesystem
COPY rootfs /

# Setup base
RUN apk add --no-cache \
    coreutils=8.31-r0 \
    wget=1.20.3-r0 \
    chromium=79.0.3945.130-r0 \
    chromium-chromedriver=79.0.3945.130-r0

RUN apk add --no-cache python3

RUN pip3 install selenium
RUN pip3 install paho-mqtt

# Build arguments
ARG BUILD_ARCH
ARG BUILD_DATE
ARG BUILD_REF
ARG BUILD_VERSION=0.0.11

# Labels
LABEL \
    io.hass.name="AlphaESS Monitor" \
    io.hass.description="AlphaESS Monitor add-on by MarioCake" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.version=${BUILD_VERSION} \
    maintainer="MarioCake <davidleinweber@web.de>" \
    org.label-schema.description="AlphaESS Monitor add-on by MarioCake" \
    org.label-schema.build-date=${BUILD_DATE} \
    org.label-schema.name="AlphaESS Monitor" \
    org.label-schema.schema-version="1.0" \
    org.label-schema.url="https://addons.community" \
    org.label-schema.usage="https://github.com/DasLetzteEinhorn/AlphaESS_Monitor_Hass/README.md" \
    org.label-schema.vcs-ref=${BUILD_REF} \
    org.label-schema.vcs-url="https://github.com/DasLetzteEinhorn/AlphaESS_Monitor_Hass" \
    org.label-schema.vendor="MarioCake"
