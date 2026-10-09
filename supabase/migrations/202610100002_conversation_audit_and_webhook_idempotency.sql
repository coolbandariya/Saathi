-- Durable audit and idempotency tables for the Saathi API.
-- Apply after 202610100001_household_memory_and_followups.sql.
-- Service-role only; do not grant browser roles access.

create table if not exists public.conversations (
    id uuid primary key default gen_random_uuid(),
    household_id uuid references public.households(id) on delete set null,
    agent_used text not null,
    user_transcript text not null,
    system_response text not null,
    tools_called jsonb not null default '[]'::jsonb,
    confidence_score double precision check (confidence_score is null or (confidence_score >= 0 and confidence_score <= 1)),
    language_code text not null default 'hi',
    correlation_id text,
    created_at timestamptz not null default now()
);

create index if not exists conversations_household_created_idx
    on public.conversations (household_id, created_at desc);
create index if not exists conversations_correlation_idx
    on public.conversations (correlation_id)
    where correlation_id is not null;

create table if not exists public.telephony_webhook_events (
    event_id text primary key,
    event_type text,
    received_at timestamptz not null default now(),
    processed_at timestamptz,
    processing_status text not null default 'received'
      check (processing_status in ('received', 'processing', 'processed', 'failed')),
    error_code text
);

alter table public.conversations enable row level security;
alter table public.telephony_webhook_events enable row level security;
revoke all on public.conversations from anon, authenticated;
revoke all on public.telephony_webhook_events from anon, authenticated;
grant all on public.conversations to service_role;
grant all on public.telephony_webhook_events to service_role;

comment on table public.conversations is
  'Minimal operational audit trail. Avoid storing unnecessary PII; define retention and deletion policy before real users.';
comment on table public.telephony_webhook_events is
  'Durable provider-event idempotency ledger. Production webhook code must atomically claim and update rows.';
