import axios from "axios";
import dayjs from "dayjs";
import { Appointment, InventoryItem, Patient, ReportOverview } from "@/types";

const api = axios.create({
  baseURL:
    process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1",
  timeout: 8000,
});

const fallbackAppointments: Appointment[] = [
  {
    id: 1,
    patient_id: 1,
    provider_id: 2,
    service_name: "Limpeza de Pele Deluxe",
    start_time: dayjs().add(1, "day").hour(10).minute(0).second(0).toISOString(),
    end_time: dayjs().add(1, "day").hour(11).minute(0).second(0).toISOString(),
    status: "confirmed",
  },
  {
    id: 2,
    patient_id: 2,
    provider_id: 2,
    service_name: "Massagem Relaxante",
    start_time: dayjs().add(1, "day").hour(14).minute(0).toISOString(),
    end_time: dayjs().add(1, "day").hour(15).minute(0).toISOString(),
    status: "pending",
  },
];

const fallbackPatients: Patient[] = [
  {
    id: 1,
    full_name: "Ana Paula",
    email: "ana@example.com",
    phone: "+55 11 99999-9999",
  },
  {
    id: 2,
    full_name: "Bruno Alves",
    email: "bruno@example.com",
    phone: "+55 11 98888-8888",
  },
];

const fallbackInventory: InventoryItem[] = [
  {
    id: 1,
    name: "Sérum Vitamina C",
    sku: "SRM-VC-01",
    quantity: 12,
    reorder_level: 8,
  },
  {
    id: 2,
    name: "Máscara Facial Detox",
    sku: "MSC-DTX-05",
    quantity: 4,
    reorder_level: 10,
  },
];

const fallbackOverview: ReportOverview = {
  total_appointments: 24,
  total_revenue: 18250,
  paid_invoices: 18,
};

export async function getAppointments(): Promise<Appointment[]> {
  try {
    const { data } = await api.get<Appointment[]>("/appointments/");
    return data;
  } catch (error) {
    console.warn("Usando dados mock de agendamentos", error);
    return fallbackAppointments;
  }
}

export async function getPatients(): Promise<Patient[]> {
  try {
    const { data } = await api.get<Patient[]>("/patients/");
    return data;
  } catch (error) {
    console.warn("Usando dados mock de pacientes", error);
    return fallbackPatients;
  }
}

export async function getInventory(): Promise<InventoryItem[]> {
  try {
    const { data } = await api.get<InventoryItem[]>("/inventory/");
    return data;
  } catch (error) {
    console.warn("Usando dados mock de estoque", error);
    return fallbackInventory;
  }
}

export async function getOverview(): Promise<ReportOverview> {
  try {
    const { data } = await api.get<ReportOverview>("/reports/overview");
    return data;
  } catch (error) {
    console.warn("Usando dados mock de relatórios", error);
    return fallbackOverview;
  }
}

export async function bookAppointment(payload: {
  patient_id: number;
  provider_id: number;
  service_name: string;
  start_time: string;
  end_time: string;
}) {
  try {
    await api.post("/appointments/", payload);
    return true;
  } catch (error) {
    console.warn("Falha ao agendar via API, simulando sucesso.", error);
    return false;
  }
}
