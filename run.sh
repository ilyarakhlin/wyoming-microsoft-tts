#!/usr/bin/with-contenv bashio

set -e

# CONFIG_PATH=/data/options.json

bashio::log.info "Loading parameters"
SUBSCRIPTION_KEY="$(bashio::config 'subscription_key')"
SERVICE_REGION="$(bashio::config 'service_region')"
CUSTOM_VOICE="$(bashio::config 'custom_voice')"
ENDPOINT_ID="$(bashio::config 'endpoint_id')"
AUDIO_FORMAT="$(bashio::config 'audio_format')"

bashio::log.info "Audio format: ${AUDIO_FORMAT}"
bashio::log.info "Custom Voice: ${CUSTOM_VOICE}"
bashio::log.info "ENDPOINT ID: ${ENDPOINT_ID}"
bashio::log.info "Sub: ${SUBSCRIPTION_KEY}"
bashio::log.info "Reg: ${SERVICE_REGION}"

python3 ./__main__.py --uri "tcp://0.0.0.0:10200" --subscription-key "${SUBSCRIPTION_KEY}" --service-region "${SERVICE_REGION}" --custom-voice "${CUSTOM_VOICE}" --endpoint-id "${ENDPOINT_ID}" --audio-format="${AUDIO_FORMAT}" --download-dir /data
