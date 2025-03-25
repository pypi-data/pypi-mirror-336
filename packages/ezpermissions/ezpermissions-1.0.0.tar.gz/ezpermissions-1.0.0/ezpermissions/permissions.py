from discord.ext import commands

class Permissions:
    """Class containing decorators for all Discord permissions."""

    def _check_permission(permission_name):
        """Base function to check user permissions dynamically."""
        class BoolWrapper:
            @staticmethod
            def True_(func):
                """Check if the user has the permission."""
                return commands.check(lambda ctx: getattr(ctx.author.guild_permissions, permission_name, False))

            @staticmethod
            def False_(func):
                """Check if the user does NOT have the permission."""
                return commands.check(lambda ctx: not getattr(ctx.author.guild_permissions, permission_name, False))

        return BoolWrapper()

    # Discord permissions as decorators
    Administrator = _check_permission("administrator")
    ManageGuild = _check_permission("manage_guild")
    ManageRoles = _check_permission("manage_roles")
    ManageChannels = _check_permission("manage_channels")
    ManageMessages = _check_permission("manage_messages")
    ManageWebhooks = _check_permission("manage_webhooks")
    ManageNicknames = _check_permission("manage_nicknames")
    ManageEmojis = _check_permission("manage_emojis")
    ManageThreads = _check_permission("manage_threads")
    ManageEvents = _check_permission("manage_events")
    BanMembers = _check_permission("ban_members")
    KickMembers = _check_permission("kick_members")
    MuteMembers = _check_permission("mute_members")
    DeafenMembers = _check_permission("deafen_members")
    MoveMembers = _check_permission("move_members")
    ModerateMembers = _check_permission("moderate_members")  # Timeout users

    ViewAuditLog = _check_permission("view_audit_log")
    ViewGuildInsights = _check_permission("view_guild_insights")
    ViewChannel = _check_permission("view_channel")

    SendMessages = _check_permission("send_messages")
    SendTTSMessages = _check_permission("send_tts_messages")
    ReadMessageHistory = _check_permission("read_message_history")
    EmbedLinks = _check_permission("embed_links")
    AttachFiles = _check_permission("attach_files")
    AddReactions = _check_permission("add_reactions")
    UseExternalEmojis = _check_permission("use_external_emojis")
    UseExternalStickers = _check_permission("use_external_stickers")
    UseApplicationCommands = _check_permission("use_application_commands")

    CreateInstantInvite = _check_permission("create_instant_invite")
    ChangeNickname = _check_permission("change_nickname")

    Connect = _check_permission("connect")
    Speak = _check_permission("speak")
    UseVAD = _check_permission("use_voice_activation")  # Voice activity detection

    PrioritySpeaker = _check_permission("priority_speaker")
    RequestToSpeak = _check_permission("request_to_speak")

    StartEmbeddedActivities = _check_permission("start_embedded_activities")

    UseSoundboard = _check_permission("use_soundboard")
    SendVoiceMessages = _check_permission("send_voice_messages")

permissions = Permissions()