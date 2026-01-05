# HACS AI Token Usage

A Home Assistant integration to monitor and track AI token usage from OpenAI. This custom component fetches usage data via the OpenAI API and exposes it as sensors in Home Assistant, allowing you to track input/output tokens and costs.

## Features

- **Real-time Monitoring**: Polls OpenAI's usage API every 15 minutes for aggregated token data.
- **Multiple Instances**: Supports multiple OpenAI accounts/orgs via separate config entries.
- **Sensors Exposed**:
  - Input Tokens: Total input tokens used in the last 24 hours.
  - Output Tokens: Total output tokens used in the last 24 hours.
  - Total Tokens: Sum of input and output tokens.
- **Configurable**: Enter your OpenAI API key and optional organization ID during setup.

## Installation

### Via HACS (Recommended)

1. Ensure [HACS](https://hacs.xyz/) is installed in your Home Assistant instance.
2. Add this repository as a custom repository in HACS:
   - Go to HACS > Integrations > Custom repositories.
   - Add `https://github.com/LauR3y/hacs-ai-token-usage` as a custom integration repository.
3. Search for "HACS AI Token Usage" in HACS and install it.
4. Restart Home Assistant.

### Manual Installation

1. Download the latest release from [GitHub Releases](https://github.com/LauR3y/hacs-ai-token-usage/releases).
2. Extract the `custom_components/hacs_ai_token_usage/` directory into your Home Assistant `config/custom_components/` folder.
3. Restart Home Assistant.

## Configuration

1. After installation, go to **Settings > Devices & Services > Add Integration** in Home Assistant.
2. Search for "HACS AI Token Usage" and select it.
3. Enter your OpenAI API key (get it from [OpenAI API Keys](https://platform.openai.com/api-keys)).
4. Optionally, enter your Organization ID (found in [OpenAI Settings](https://platform.openai.com/account/org-settings)).
5. Click "Submit" to complete setup.
6. Sensors will appear under the integration's device.

## Usage

- **Sensors**: The integration creates three sensors per config entry, displaying token counts.
- **Dashboard**: Add these sensors to your Home Assistant dashboard for monitoring usage.
- **Automation**: Use the sensor values in automations (e.g., alerts when nearing limits).

## Requirements

- Home Assistant 2021.12.0 or later.
- A valid OpenAI API key with admin access for usage data.

## Support

- **Issues**: Report bugs or request features at [GitHub Issues](https://github.com/LauR3y/hacs-ai-token-usage/issues).
- **Documentation**: See the [GitHub Repo](https://github.com/LauR3y/hacs-ai-token-usage) for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.