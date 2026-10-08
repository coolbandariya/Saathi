-- Saathi core persistence schema.
-- Apply only to the Saathi Supabase project after authentication/ownership
-- configuration has been verified. This migration intentionally stores
-- metadata and consent state, not raw sensitive document contents.

create extension if not exists pgcrypto;

create table if not exists public.households (
  id uuid primary key default gen_random_uuid(),
  owner_user_id uuid not null references auth.users(id) on delete cascade,
  display_name text,
  created_at timestamptz not null default now()
);

create table if not exists public.consents (
  id uuid primary key default gen_random_uuid(),
  household_id uuid not null references public.households(id) on delete cascade,
  consent_type text not null check (consent_type in ('memory','outbound_calls','document_processing','recording')),
  granted boolean not null,
  recorded_at timestamptz not null default now(),
  unique (household_id, consent_type)
);

create table if not exists public.tasks (
  id uuid primary key default gen_random_uuid(),
  household_id uuid not null references public.households(id) on delete cascade,
  title text not null check (char_length(title) between 1 and 300),
  status text not null default 'pending' check (status in ('pending','completed','cancelled','escalated')),
  missing_items jsonb not null default '[]'::jsonb,
  scheduled_callback timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.conversations (
  id uuid primary key default gen_random_uuid(),
  household_id uuid not null references public.households(id) on delete cascade,
  role text not null check (role in ('user','assistant','system')),
  message text not null check (char_length(message) <= 4000),
  language text not null default 'hi',
  created_at timestamptz not null default now()
);

create table if not exists public.webhook_events (
  event_id text primary key,
  provider text not null,
  received_at timestamptz not null default now(),
  payload_hash text
);

create index if not exists idx_consents_household on public.consents(household_id);
create index if not exists idx_tasks_household_status on public.tasks(household_id, status);
create index if not exists idx_conversations_household_created on public.conversations(household_id, created_at desc);

alter table public.households enable row level security;
alter table public.consents enable row level security;
alter table public.tasks enable row level security;
alter table public.conversations enable row level security;
alter table public.webhook_events enable row level security;

create policy "households_owner_select" on public.households
  for select using (owner_user_id = auth.uid());

create policy "households_owner_insert" on public.households
  for insert with check (owner_user_id = auth.uid());

create policy "households_owner_update" on public.households
  for update using (owner_user_id = auth.uid()) with check (owner_user_id = auth.uid());

create policy "consents_owner_all" on public.consents
  for all using (
    exists (
      select 1 from public.households h
      where h.id = household_id and h.owner_user_id = auth.uid()
    )
  ) with check (
    exists (
      select 1 from public.households h
      where h.id = household_id and h.owner_user_id = auth.uid()
    )
  );

create policy "tasks_owner_all" on public.tasks
  for all using (
    exists (
      select 1 from public.households h
      where h.id = household_id and h.owner_user_id = auth.uid()
    )
  ) with check (
    exists (
      select 1 from public.households h
      where h.id = household_id and h.owner_user_id = auth.uid()
    )
  );

create policy "conversations_owner_all" on public.conversations
  for all using (
    exists (
      select 1 from public.households h
      where h.id = household_id and h.owner_user_id = auth.uid()
    )
  ) with check (
    exists (
      select 1 from public.households h
      where h.id = household_id and h.owner_user_id = auth.uid()
    )
  );

-- Webhook idempotency is server-owned and must not be exposed to clients.
revoke all on public.webhook_events from anon, authenticated;

create or replace function public.touch_task_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists tasks_touch_updated_at on public.tasks;
create trigger tasks_touch_updated_at
before update on public.tasks
for each row execute function public.touch_task_updated_at();
