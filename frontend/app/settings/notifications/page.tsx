'use client';

import { useState, useEffect } from 'react';
import { Bell, Mail, MessageSquare, Send, Check, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { useToast } from '@/components/ui/use-toast';

interface NotificationSettings {
  id: number;
  user_id: number;
  slack_webhook: string | null;
  discord_webhook: string | null;
  email_enabled: boolean;
  whatsapp_enabled: boolean;
  notify_on_failure: boolean;
  notify_on_success: boolean;
  notify_on_completion: boolean;
  created_at: string;
  updated_at: string;
}

export default function NotificationsSettingsPage() {
  const { toast } = useToast();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [slackWebhook, setSlackWebhook] = useState('');
  const [discordWebhook, setDiscordWebhook] = useState('');
  const [emailEnabled, setEmailEnabled] = useState(true);
  const [whatsappEnabled, setWhatsappEnabled] = useState(false);
  const [notifyOnFailure, setNotifyOnFailure] = useState(true);
  const [notifyOnSuccess, setNotifyOnSuccess] = useState(false);
  const [notifyOnCompletion, setNotifyOnCompletion] = useState(true);

  useEffect(() => {
    fetchSettings();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const fetchSettings = async () => {
    try {
      const response = await fetch('/api/notifications/settings', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      });
      const data: NotificationSettings = await response.json();
      setSlackWebhook(data.slack_webhook || '');
      setDiscordWebhook(data.discord_webhook || '');
      setEmailEnabled(data.email_enabled);
      setWhatsappEnabled(data.whatsapp_enabled);
      setNotifyOnFailure(data.notify_on_failure);
      setNotifyOnSuccess(data.notify_on_success);
      setNotifyOnCompletion(data.notify_on_completion);
    } catch (error) {
      console.error('Error fetching notification settings:', error);
      toast({
        title: 'Error',
        description: 'Failed to load notification settings',
        variant: 'destructive',
      });
    } finally {
      setLoading(false);
    }
  };

  const saveSettings = async () => {
    setSaving(true);
    try {
      const response = await fetch('/api/notifications/settings', {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
        body: JSON.stringify({
          slack_webhook: slackWebhook || null,
          discord_webhook: discordWebhook || null,
          email_enabled: emailEnabled,
          whatsapp_enabled: whatsappEnabled,
          notify_on_failure: notifyOnFailure,
          notify_on_success: notifyOnSuccess,
          notify_on_completion: notifyOnCompletion,
        }),
      });

      if (response.ok) {
        toast({
          title: 'Success',
          description: 'Notification settings saved successfully',
        });
        fetchSettings();
      } else {
        throw new Error('Failed to save settings');
      }
    } catch (error) {
      console.error('Error saving notification settings:', error);
      toast({
        title: 'Error',
        description: 'Failed to save notification settings',
        variant: 'destructive',
      });
    } finally {
      setSaving(false);
    }
  };

  const testNotification = async (channel: string) => {
    try {
      const response = await fetch('/api/notifications/test', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
        body: JSON.stringify({ channel }),
      });

      if (response.ok) {
        toast({
          title: 'Test Sent',
          description: `Test notification sent to ${channel}`,
        });
      } else {
        const error = await response.json();
        throw new Error(error.detail);
      }
    } catch (error: unknown) {
      const err = error as Error;
      toast({
        title: 'Test Failed',
        description: err.message || 'Failed to send test notification',
        variant: 'destructive',
      });
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-6 space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Notification Settings</h1>
        <p className="text-muted-foreground">
          Configure how you want to be notified about test runs
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Notification Channels</CardTitle>
          <CardDescription>
            Set up integrations with your preferred communication tools
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Slack Integration */}
          <div className="space-y-3">
            <div className="flex items-center gap-3">
              <MessageSquare className="h-5 w-5 text-purple-500" />
              <Label htmlFor="slack-webhook" className="text-base font-semibold">
                Slack
              </Label>
            </div>
            <div className="flex gap-2">
              <Input
                id="slack-webhook"
                type="url"
                placeholder="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
                value={slackWebhook}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => setSlackWebhook(e.target.value)}
                className="flex-1"
              />
              <Button
                variant="outline"
                onClick={() => testNotification('slack')}
                disabled={!slackWebhook}
              >
                <Send className="h-4 w-4" />
              </Button>
            </div>
            <p className="text-sm text-muted-foreground">
              Create a webhook in Slack: Workspace Settings → Apps → Incoming Webhooks
            </p>
          </div>

          {/* Discord Integration */}
          <div className="space-y-3">
            <div className="flex items-center gap-3">
              <MessageSquare className="h-5 w-5 text-indigo-500" />
              <Label htmlFor="discord-webhook" className="text-base font-semibold">
                Discord
              </Label>
            </div>
            <div className="flex gap-2">
              <Input
                id="discord-webhook"
                type="url"
                placeholder="https://discord.com/api/webhooks/YOUR/WEBHOOK/URL"
                value={discordWebhook}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => setDiscordWebhook(e.target.value)}
                className="flex-1"
              />
              <Button
                variant="outline"
                onClick={() => testNotification('discord')}
                disabled={!discordWebhook}
              >
                <Send className="h-4 w-4" />
              </Button>
            </div>
            <p className="text-sm text-muted-foreground">
              Create a webhook in Discord: Server Settings → Integrations → Webhooks
            </p>
          </div>

          {/* Email Integration */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <Mail className="h-5 w-5 text-blue-500" />
                <Label htmlFor="email-enabled" className="text-base font-semibold">
                  Email Notifications
                </Label>
              </div>
              <div className="flex items-center gap-2">
                <Switch
                  id="email-enabled"
                  checked={emailEnabled}
                  onCheckedChange={setEmailEnabled}
                />
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => testNotification('email')}
                  disabled={!emailEnabled}
                >
                  <Send className="h-4 w-4" />
                </Button>
              </div>
            </div>
            <p className="text-sm text-muted-foreground">
              Receive notifications via email to your registered address
            </p>
          </div>

          {/* WhatsApp Integration */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <MessageSquare className="h-5 w-5 text-green-500" />
                <Label htmlFor="whatsapp-enabled" className="text-base font-semibold">
                  WhatsApp Notifications
                </Label>
              </div>
              <div className="flex items-center gap-2">
                <Switch
                  id="whatsapp-enabled"
                  checked={whatsappEnabled}
                  onCheckedChange={setWhatsappEnabled}
                  disabled
                />
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => testNotification('whatsapp')}
                  disabled
                >
                  <Send className="h-4 w-4" />
                </Button>
              </div>
            </div>
            <p className="text-sm text-muted-foreground">
              WhatsApp integration coming soon (requires Twilio setup)
            </p>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Notification Preferences</CardTitle>
          <CardDescription>
            Choose when you want to receive notifications
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between p-4 border rounded-lg">
            <div className="space-y-0.5">
              <div className="flex items-center gap-2">
                <X className="h-4 w-4 text-red-500" />
                <Label htmlFor="notify-failure" className="font-medium">
                  Notify on Test Failures
                </Label>
              </div>
              <p className="text-sm text-muted-foreground">
                Get notified when test runs fail
              </p>
            </div>
            <Switch
              id="notify-failure"
              checked={notifyOnFailure}
              onCheckedChange={setNotifyOnFailure}
            />
          </div>

          <div className="flex items-center justify-between p-4 border rounded-lg">
            <div className="space-y-0.5">
              <div className="flex items-center gap-2">
                <Check className="h-4 w-4 text-green-500" />
                <Label htmlFor="notify-success" className="font-medium">
                  Notify on Test Success
                </Label>
              </div>
              <p className="text-sm text-muted-foreground">
                Get notified when all tests pass
              </p>
            </div>
            <Switch
              id="notify-success"
              checked={notifyOnSuccess}
              onCheckedChange={setNotifyOnSuccess}
            />
          </div>

          <div className="flex items-center justify-between p-4 border rounded-lg">
            <div className="space-y-0.5">
              <div className="flex items-center gap-2">
                <Bell className="h-4 w-4 text-blue-500" />
                <Label htmlFor="notify-completion" className="font-medium">
                  Notify on Completion
                </Label>
              </div>
              <p className="text-sm text-muted-foreground">
                Get notified when test runs complete, regardless of result
              </p>
            </div>
            <Switch
              id="notify-completion"
              checked={notifyOnCompletion}
              onCheckedChange={setNotifyOnCompletion}
            />
          </div>
        </CardContent>
      </Card>

      <div className="flex justify-end gap-3">
        <Button variant="outline" onClick={fetchSettings}>
          Reset
        </Button>
        <Button onClick={saveSettings} disabled={saving}>
          {saving ? 'Saving...' : 'Save Settings'}
        </Button>
      </div>
    </div>
  );
}