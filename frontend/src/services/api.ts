import { AssessmentResponse, SymptomAssessmentRequest } from '../types';

const API_BASE = '/api';

export async function checkHealth(): Promise<{ status: string; ai_enabled: boolean; service: string }> {
  try {
    const res = await fetch(`${API_BASE}/health`, {
      method: 'GET',
      headers: { 'Accept': 'application/json' },
    });
    if (!res.ok) {
      throw new Error(`Health check failed with status: ${res.status}`);
    }
    return await res.json();
  } catch (err) {
    console.warn('API health check error:', err);
    throw err;
  }
}

export async function assessSymptoms(
  payload: SymptomAssessmentRequest
): Promise<AssessmentResponse> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 12000); // 12 second client timeout

  try {
    const response = await fetch(`${API_BASE}/assess`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify(payload),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      const errBody = await response.json().catch(() => ({}));
      const msg = errBody.message || errBody.details?.[0] || `Server error (${response.status})`;
      throw new Error(msg);
    }

    return await response.json();
  } catch (err: any) {
    clearTimeout(timeoutId);
    if (err.name === 'AbortError') {
      throw new Error('Assessment request timed out. Please check your backend connection.');
    }
    throw err;
  }
}
