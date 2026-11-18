-- COMEBACK training workflow. Every table is scoped to the existing patient
-- connection; historical unit snapshots are never overwritten by new plans.
create table if not exists public.training_plan_versions (
  id uuid primary key default gen_random_uuid(),
  patient_record_id text not null references public.patient_records(id) on delete cascade,
  phase smallint not null check (phase between 1 and 5),
  version integer not null,
  status text not null default 'draft' check (status in ('draft','published','superseded')),
  source_page text,
  change_note text,
  finding_id text,
  payload jsonb not null default '{}'::jsonb,
  created_by uuid not null references auth.users(id),
  created_at timestamptz not null default timezone('utc', now()),
  unique(patient_record_id, version)
);

create table if not exists public.training_units (
  id uuid primary key default gen_random_uuid(),
  patient_record_id text not null references public.patient_records(id) on delete cascade,
  plan_version_id uuid not null references public.training_plan_versions(id) on delete restrict,
  phase smallint not null check (phase between 1 and 5),
  scheduled_for date not null,
  title text not null,
  status text not null default 'planned' check (status in ('planned','in_progress','completed','missed')),
  exercise_ids text[] not null default '{}',
  completed_count integer,
  completion_key text unique,
  rescheduled_from date,
  started_at timestamptz,
  completed_at timestamptz,
  created_at timestamptz not null default timezone('utc', now())
);

create table if not exists public.exercise_logs (
  id uuid primary key default gen_random_uuid(),
  training_unit_id uuid not null references public.training_units(id) on delete cascade,
  exercise_id text not null,
  status text not null check (status in ('done','skipped')),
  reason text,
  note text,
  created_at timestamptz not null default timezone('utc', now()),
  unique(training_unit_id, exercise_id)
);

create table if not exists public.training_feedback (
  id uuid primary key default gen_random_uuid(),
  training_unit_id uuid not null references public.training_units(id) on delete cascade,
  exercise_id text,
  author_id uuid not null references auth.users(id),
  text text not null,
  reply text,
  reviewed_at timestamptz,
  created_at timestamptz not null default timezone('utc', now()),
  replied_at timestamptz
);

alter table public.training_plan_versions enable row level security;
alter table public.training_units enable row level security;
alter table public.exercise_logs enable row level security;
alter table public.training_feedback enable row level security;

-- The patient_records row is the single source of connection truth. No client
-- can address another patient by guessing an id.
create policy "connected users read plan versions" on public.training_plan_versions
  for select to authenticated using (exists (select 1 from public.patient_records r where r.id=patient_record_id and (auth.uid()=r.patient_user_id or auth.uid()=r.clinician_user_id)));
create policy "connected clinicians write plan versions" on public.training_plan_versions
  for all to authenticated using (exists (select 1 from public.patient_records r where r.id=patient_record_id and auth.uid()=r.clinician_user_id)) with check (exists (select 1 from public.patient_records r where r.id=patient_record_id and auth.uid()=r.clinician_user_id));

create policy "connected users read units" on public.training_units
  for select to authenticated using (exists (select 1 from public.patient_records r where r.id=patient_record_id and (auth.uid()=r.patient_user_id or auth.uid()=r.clinician_user_id)));
create policy "connected clinicians write units" on public.training_units
  for all to authenticated using (exists (select 1 from public.patient_records r where r.id=patient_record_id and auth.uid()=r.clinician_user_id)) with check (exists (select 1 from public.patient_records r where r.id=patient_record_id and auth.uid()=r.clinician_user_id));

create policy "connected users read logs" on public.exercise_logs
  for select to authenticated using (exists (select 1 from public.training_units u join public.patient_records r on r.id=u.patient_record_id where u.id=training_unit_id and (auth.uid()=r.patient_user_id or auth.uid()=r.clinician_user_id)));
create policy "patients write own logs" on public.exercise_logs
  for insert to authenticated with check (exists (select 1 from public.training_units u join public.patient_records r on r.id=u.patient_record_id where u.id=training_unit_id and auth.uid()=r.patient_user_id));

create policy "connected users read feedback" on public.training_feedback
  for select to authenticated using (exists (select 1 from public.training_units u join public.patient_records r on r.id=u.patient_record_id where u.id=training_unit_id and (auth.uid()=r.patient_user_id or auth.uid()=r.clinician_user_id)));
create policy "patients create feedback" on public.training_feedback
  for insert to authenticated with check (author_id=auth.uid() and exists (select 1 from public.training_units u join public.patient_records r on r.id=u.patient_record_id where u.id=training_unit_id and auth.uid()=r.patient_user_id));
create policy "clinicians answer feedback" on public.training_feedback
  for update to authenticated using (exists (select 1 from public.training_units u join public.patient_records r on r.id=u.patient_record_id where u.id=training_unit_id and auth.uid()=r.clinician_user_id)) with check (exists (select 1 from public.training_units u join public.patient_records r on r.id=u.patient_record_id where u.id=training_unit_id and auth.uid()=r.clinician_user_id));
