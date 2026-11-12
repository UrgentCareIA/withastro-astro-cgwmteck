-- VillageTech : table des demandes d'accès à la bêta.
-- À coller dans Supabase > SQL Editor > New query, puis "Run".

create table if not exists public.beta_requests (
  id                   uuid primary key default gen_random_uuid(),
  created_at           timestamptz not null default now(),
  first_name           text not null check (char_length(first_name) between 1 and 80),
  last_name            text not null check (char_length(last_name) between 1 and 80),
  email                text not null unique check (email ~* '^[^@\s]+@[^@\s]+\.[^@\s]+$'),
  higgsfield_username  text not null check (char_length(higgsfield_username) between 1 and 80),
  company              text check (char_length(company) <= 120),
  stage                text not null check (stage in ('idee','lancement','activite','croissance','autre')),
  sector               text check (char_length(sector) <= 80),
  motivation           text not null check (char_length(motivation) between 1 and 1000),
  referral             text check (char_length(referral) <= 120),
  -- Suivi interne : à changer à la main dans le Table Editor
  status               text not null default 'en_attente'
                       check (status in ('en_attente','valide','refuse')),
  validated_at         timestamptz,
  notes                text
);

-- Sécurité : le site public peut UNIQUEMENT ajouter une demande.
-- Personne ne peut lire, modifier ou supprimer la liste depuis le site.
-- Vous la consultez depuis le dashboard Supabase (qui contourne ces règles).
alter table public.beta_requests enable row level security;

drop policy if exists "public peut s'inscrire" on public.beta_requests;
create policy "public peut s'inscrire"
  on public.beta_requests
  for insert
  to anon
  with check (status = 'en_attente' and validated_at is null and notes is null);

revoke all on public.beta_requests from anon;
grant insert (first_name, last_name, email, higgsfield_username, company, stage, sector, motivation, referral)
  on public.beta_requests to anon;

-- Remplit validated_at automatiquement quand vous passez une demande en "valide".
create or replace function public.beta_requests_set_validated_at()
returns trigger language plpgsql as $$
begin
  if new.status = 'valide' and old.status is distinct from 'valide' then
    new.validated_at := now();
  end if;
  return new;
end $$;

drop trigger if exists trg_beta_requests_validated on public.beta_requests;
create trigger trg_beta_requests_validated
  before update on public.beta_requests
  for each row execute function public.beta_requests_set_validated_at();

-- Vue pratique : les demandes à traiter, les plus anciennes d'abord.
create or replace view public.beta_a_traiter
  with (security_invoker = true) as
  select created_at, first_name, last_name, email, higgsfield_username, stage, company, motivation
  from public.beta_requests
  where status = 'en_attente'
  order by created_at;
