create table if not exists public.patient_records (
  id text primary key,
  patient_user_id uuid not null references auth.users(id) on delete cascade,
  clinician_user_id uuid not null references auth.users(id) on delete restrict,
  payload jsonb not null,
  updated_at timestamptz not null default timezone('utc', now())
);

alter table public.patient_records enable row level security;

create policy "patients read their own record"
  on public.patient_records for select
  to authenticated
  using (auth.uid() = patient_user_id);

create policy "clinicians read connected records"
  on public.patient_records for select
  to authenticated
  using (auth.uid() = clinician_user_id);

create policy "clinicians create connected records"
  on public.patient_records for insert
  to authenticated
  with check (auth.uid() = clinician_user_id);

create policy "clinicians update connected records"
  on public.patient_records for update
  to authenticated
  using (auth.uid() = clinician_user_id)
  with check (auth.uid() = clinician_user_id);

create policy "patients update only their own consent fields"
  on public.patient_records for update
  to authenticated
  using (auth.uid() = patient_user_id)
  with check (auth.uid() = patient_user_id);

create or replace function public.touch_patient_records_updated_at()
returns trigger language plpgsql security invoker as $$
begin
  new.updated_at = timezone('utc', now());
  return new;
end;
$$;

drop trigger if exists patient_records_updated_at on public.patient_records;
create trigger patient_records_updated_at
before update on public.patient_records
for each row execute function public.touch_patient_records_updated_at();

alter table public.patient_records replica identity full;
alter publication supabase_realtime add table public.patient_records;
