const url = (import.meta.env.VITE_SUPABASE_URL as string | undefined)?.replace(/\/$/, '');
const anonKey = import.meta.env.VITE_SUPABASE_ANON_KEY as string | undefined;

/** Optional REST adapter. It stays disabled until both public project values exist. */
export const backendConfigured = Boolean(url && anonKey);
type PatientRecord = { id: string; payload: Record<string, unknown>; updated_at: string };

async function request<T>(path: string, init: RequestInit = {}) {
  if (!url || !anonKey) return null;
  const response = await fetch(`${url}/rest/v1/${path}`, {
    ...init,
    headers: { apikey: anonKey, Authorization: `Bearer ${anonKey}`, 'Content-Type': 'application/json', Prefer: 'return=representation', ...(init.headers || {}) }
  });
  if (!response.ok) throw new Error(`Supabase ${response.status}`);
  return response.status === 204 ? null : response.json() as Promise<T>;
}

export async function fetchPatientRecord(id: string) {
  const rows = await request<PatientRecord[]>(`patient_records?select=id,payload,updated_at&id=eq.${encodeURIComponent(id)}&limit=1`);
  return rows?.[0] || null;
}

export async function upsertPatientRecord(id: string, payload: Record<string, unknown>) {
  await request('patient_records', { method: 'POST', headers: { Prefer: 'resolution=merge-duplicates,return=minimal' }, body: JSON.stringify({ id, payload }) });
}

/** REST has no websocket dependency here; callers can poll this safely. */
export function subscribeToPatientRecord(_id: string, _onChange: () => void) { return () => undefined; }
