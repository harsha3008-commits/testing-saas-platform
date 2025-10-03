-- Notification Settings Schema
-- Run this to add notification settings table

CREATE TABLE IF NOT EXISTS notification_settings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    slack_webhook VARCHAR(500),
    discord_webhook VARCHAR(500),
    email_enabled BOOLEAN DEFAULT true,
    whatsapp_enabled BOOLEAN DEFAULT false,
    notify_on_failure BOOLEAN DEFAULT true,
    notify_on_success BOOLEAN DEFAULT false,
    notify_on_completion BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_notification_settings_user_id ON notification_settings(user_id);

-- Update trigger for notification_settings
CREATE OR REPLACE FUNCTION update_notification_settings_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER notification_settings_updated_at
    BEFORE UPDATE ON notification_settings
    FOR EACH ROW
    EXECUTE FUNCTION update_notification_settings_timestamp();

COMMENT ON TABLE notification_settings IS 'User notification preferences for test run alerts';
COMMENT ON COLUMN notification_settings.slack_webhook IS 'Slack incoming webhook URL';
COMMENT ON COLUMN notification_settings.discord_webhook IS 'Discord webhook URL';
COMMENT ON COLUMN notification_settings.email_enabled IS 'Enable email notifications';
COMMENT ON COLUMN notification_settings.whatsapp_enabled IS 'Enable WhatsApp notifications (requires Twilio)';
COMMENT ON COLUMN notification_settings.notify_on_failure IS 'Send notification when tests fail';
COMMENT ON COLUMN notification_settings.notify_on_success IS 'Send notification when tests pass';
COMMENT ON COLUMN notification_settings.notify_on_completion IS 'Send notification on test completion regardless of result';