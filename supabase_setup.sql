-- Chạy toàn bộ SQL này trong Supabase: SQL Editor > New query > Run
create table if not exists public.rooms (
  code text primary key,
  max_players integer not null default 40,
  current_question_id text,
  called_player_id text,
  status text not null default 'lobby'
);
create table if not exists public.players (
  id text primary key,
  room_code text not null references public.rooms(code) on delete cascade,
  name text not null,
  role text not null default 'Học sinh',
  score integer not null default 0,
  joined_at timestamptz default now()
);
create table if not exists public.questions (
  id text primary key,
  room_code text not null references public.rooms(code) on delete cascade,
  question text not null,
  options jsonb not null,
  correct_index integer not null default 0,
  active boolean not null default true,
  created_at timestamptz default now()
);
create table if not exists public.answers (
  id text primary key,
  room_code text not null references public.rooms(code) on delete cascade,
  question_id text not null references public.questions(id) on delete cascade,
  player_id text not null references public.players(id) on delete cascade,
  player_name text not null,
  choice text not null,
  correct boolean not null default false,
  created_at timestamptz default now()
);

-- Demo đơn giản: bật RLS và policy cho anon để lớp có thể dùng.
-- Với môi trường thật, cần thêm xác thực giáo viên và giới hạn quyền ghi.
alter table public.rooms enable row level security;
alter table public.players enable row level security;
alter table public.questions enable row level security;
alter table public.answers enable row level security;

create policy "rooms demo access" on public.rooms for all to anon using (true) with check (true);
create policy "players demo access" on public.players for all to anon using (true) with check (true);
create policy "questions demo access" on public.questions for all to anon using (true) with check (true);
create policy "answers demo access" on public.answers for all to anon using (true) with check (true);
