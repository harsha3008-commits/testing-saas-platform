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
      <div className="flex items-center justify-center min-h-screen bg-black">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black text-white">
      <div className="container mx-auto p-6 space-y-8">
        <div>
          <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
            Notification Settings
          </h1>
          <p className="text-gray-400 mt-2">
            Configure how you want to be notified about test runs
          </p>
        </div>

        <Card className="bg-gradient-to-br from-gray-900 to-gray-800 border-gray-800">
          <CardHeader>
            <CardTitle className="text-white text-2xl">Notification Channels</CardTitle>
            <CardDescription className="text-gray-400">
              Set up integrations with your preferred communication tools
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Slack Integration */}
            <div className="space-y-3 p-4 bg-black/40 rounded-xl border border-gray-800 hover:border-purple-500/50 transition-all">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-purple-500/20 rounded-lg">
                  <MessageSquare className="h-5 w-5 text-purple-400" />
                </div>
                <Label htmlFor="slack-webhook" className="text-base font-semibold text-white">
                  Slack Integration
                </Label>
              </div>
              <div className="flex gap-2">
                <Input
                  id="slack-webhook"
                  type="url"
                  placeholder="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
                  value={slackWebhook}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) => setSlackWebhook(e.target.value)}
                  className="flex-1 bg-black border-gray-800 text-white placeholder:text-gray-600"
                />
                <Button
                  variant="outline"
                  onClick={() => testNotification('slack')}
                  disabled={!slackWebhook}
                  className="border-gray-700 hover:border-purple-500 hover:bg-purple-500/20"
                >
                  <Send className="h-4 w-4" />
                </Button>
              </div>
              <p className="text-sm text-gray-500">
                Create a webhook in Slack: Workspace Settings → Apps → Incoming Webhooks
              </p>
            </div>

            {/* Discord Integration */}
            <div className="space-y-3 p-4 bg-black/40 rounded-xl border border-gray-800 hover:border-pink-500/50 transition-all">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-pink-500/20 rounded-lg">
                  <MessageSquare className="h-5 w-5 text-pink-400" />
                </div>
                <Label htmlFor="discord-webhook" className="text-base font-semibold text-white">
                  Discord Integration
                </Label>
              </div>
              <div className="flex gap-2">
                <Input
                  id="discord-webhook"
                  type="url"
                  placeholder="https://discord.com/api/webhooks/YOUR/WEBHOOK/URL"
                  value={discordWebhook}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) => setDiscordWebhook(e.target.value)}
                  className="flex-1 bg-black border-gray-800 text-white placeholder:text-gray-600"
                />
                <Button
                  variant="outline"
                  onClick={() => testNotification('discord')}
                  disabled={!discordWebhook}
                  className="border-gray-700 hover:border-pink-500 hover:bg-pink-500/20"
                >
                  <Send className="h-4 w-4" />
                </Button>
              </div>
              <p className="text-sm text-gray-500">
                Create a webhook in Discord: Server Settings → Integrations → Webhooks
              </p>
            </div>

            {/* Email Integration */}
            <div className="space-y-3 p-4 bg-black/40 rounded-xl border border-gray-800 hover:border-blue-500/50 transition-all">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-blue-500/20 rounded-lg">
                    <Mail className="h-5 w-5 text-blue-400" />
                  </div>
                  <Label htmlFor="email-enabled" className="text-base font-semibold text-white">
                    Email Notifications
                  </Label>
                </div>
                <div className="flex items-center gap-2">
                  <Switch
                    id="email-enabled"
                    checked={emailEnabled}
                    onCheckedChange={setEmailEnabled}
                    className="data-[state=checked]:bg-gradient-to-r data-[state=checked]:from-purple-500 data-[state=checked]:to-pink-500"
                  />
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => testNotification('email')}
                    disabled={!emailEnabled}
                    className="border-gray-700 hover:border-blue-500 hover:bg-blue-500/20"
                  >
                    <Send className="h-4 w-4" />
                  </Button>
                </div>
              </div>
              <p className="text-sm text-gray-500">
                Receive notifications via email to your registered address
              </p>
            </div>

            {/* WhatsApp Integration */}
            <div className="space-y-3 p-4 bg-black/40 rounded-xl border border-gray-800 opacity-60">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-green-500/20 rounded-lg">
                    <MessageSquare className="h-5 w-5 text-green-400" />
                  </div>
                  <Label htmlFor="whatsapp-enabled" className="text-base font-semibold text-white">
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
                    className="border-gray-700"
                  >
                    <Send className="h-4 w-4" />
                  </Button>
                </div>
              </div>
              <p className="text-sm text-gray-500">
                WhatsApp integration coming soon (requires Twilio setup)
              </p>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-gray-900 to-gray-800 border-gray-800">
          <CardHeader>
            <CardTitle className="text-white text-2xl">Notification Preferences</CardTitle>
            <CardDescription className="text-gray-400">
              Choose when you want to receive notifications
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex items-center justify-between p-5 bg-black/40 border border-gray-800 rounded-xl hover:border-red-500/50 transition-all">
              <div className="space-y-0.5">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-red-500/20 rounded-lg">
                    <X className="h-4 w-4 text-red-400" />
                  </div>
                  <Label htmlFor="notify-failure" className="font-semibold text-white cursor-pointer">
                    Notify on Test Failures
                  </Label>
                </div>
                <p className="text-sm text-gray-500 ml-11">
                  Get notified when test runs fail
                </p>
              </div>
              <Switch
                id="notify-failure"
                checked={notifyOnFailure}
                onCheckedChange={setNotifyOnFailure}
                className="data-[state=checked]:bg-gradient-to-r data-[state=checked]:from-purple-500 data-[state=checked]:to-pink-500"
              />
            </div>

            <div className="flex items-center justify-between p-5 bg-black/40 border border-gray-800 rounded-xl hover:border-green-500/50 transition-all">
              <div className="space-y-0.5">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-green-500/20 rounded-lg">
                    <Check className="h-4 w-4 text-green-400" />
                  </div>
                  <Label htmlFor="notify-success" className="font-semibold text-white cursor-pointer">
                    Notify on Test Success
                  </Label>
                </div>
                <p className="text-sm text-gray-500 ml-11">
                  Get notified when all tests pass
                </p>
              </div>
              <Switch
                id="notify-success"
                checked={notifyOnSuccess}
                onCheckedChange={setNotifyOnSuccess}
                className="data-[state=checked]:bg-gradient-to-r data-[state=checked]:from-purple-500 data-[state=checked]:to-pink-500"
              />
            </div>

            <div className="flex items-center justify-between p-5 bg-black/40 border border-gray-800 rounded-xl hover:border-blue-500/50 transition-all">
              <div className="space-y-0.5">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-blue-500/20 rounded-lg">
                    <Bell className="h-4 w-4 text-blue-400" />
                  </div>
                  <Label htmlFor="notify-completion" className="font-semibold text-white cursor-pointer">
                    Notify on Completion
                  </Label>
                </div>
                <p className="text-sm text-gray-500 ml-11">
                  Get notified when test runs complete, regardless of result
                </p>
              </div>
              <Switch
                id="notify-completion"
                checked={notifyOnCompletion}
                onCheckedChange={setNotifyOnCompletion}
                className="data-[state=checked]:bg-gradient-to-r data-[state=checked]:from-purple-500 data-[state=checked]:to-pink-500"
              />
            </div>
          </CardContent>
        </Card>

        <div className="flex justify-end gap-3">
          <Button 
            variant="outline" 
            onClick={fetchSettings}
            className="border-gray-700 hover:border-gray-600 hover:bg-gray-800"
          >
            Reset
          </Button>
          <Button 
            onClick={saveSettings} 
            disabled={saving}
            className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white font-semibold"
          >
            {saving ? 'Saving...' : 'Save Settings'}
          </Button>
        </div>
      </div>
    </div>
  );
}