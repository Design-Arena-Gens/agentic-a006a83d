'use client';

import { useState } from "react";
import { useForm } from "react-hook-form";
import { useQuery } from "@tanstack/react-query";
import dayjs from "dayjs";
import { useTranslation } from "react-i18next";
import { bookAppointment, getPatients } from "@/services/api";

type AppointmentForm = {
  patient_id: number;
  service_name: string;
  date: string;
  time: string;
};

const services = [
  "Limpeza de Pele",
  "Peeling Químico",
  "Massagem Relaxante",
  "Depilação a Laser",
];

export function PatientPortalView() {
  const { t } = useTranslation();
  const { data: patients = [] } = useQuery({
    queryKey: ["patients"],
    queryFn: getPatients,
  });
  const [status, setStatus] = useState<"idle" | "success" | "error">("idle");

  const { register, handleSubmit, reset } = useForm<AppointmentForm>({
    defaultValues: {
      patient_id: patients[0]?.id ?? 1,
      service_name: services[0],
      date: dayjs().add(1, "day").format("YYYY-MM-DD"),
      time: "10:00",
    },
  });

  const onSubmit = handleSubmit(async (formData) => {
    setStatus("idle");
    const start = dayjs(`${formData.date} ${formData.time}`);
    const success = await bookAppointment({
      patient_id: Number(formData.patient_id),
      provider_id: 1,
      service_name: formData.service_name,
      start_time: start.toISOString(),
      end_time: start.add(1, "hour").toISOString(),
    });
    setStatus(success ? "success" : "error");
    reset();
  });

  return (
    <div className="card space-y-6">
      <header>
        <h2 className="text-2xl font-semibold text-slate-800">{t("patient_portal")}</h2>
        <p className="text-sm text-slate-500">
          Agende seu próximo tratamento, gerencie pagamentos e acompanhe seu histórico.
        </p>
      </header>

      <form onSubmit={onSubmit} className="grid gap-4 md:grid-cols-2">
        <label className="flex flex-col gap-1 text-sm font-medium text-slate-700">
          Paciente
          <select
            {...register("patient_id", { required: true })}
            className="rounded-xl border border-slate-200 px-3 py-2 text-sm shadow-sm focus:border-brand-400 focus:outline-none"
          >
            {patients.map((patient) => (
              <option key={patient.id} value={patient.id}>
                {patient.full_name}
              </option>
            ))}
          </select>
        </label>

        <label className="flex flex-col gap-1 text-sm font-medium text-slate-700">
          Tratamento
          <select
            {...register("service_name", { required: true })}
            className="rounded-xl border border-slate-200 px-3 py-2 text-sm shadow-sm focus:border-brand-400 focus:outline-none"
          >
            {services.map((service) => (
              <option key={service} value={service}>
                {service}
              </option>
            ))}
          </select>
        </label>

        <label className="flex flex-col gap-1 text-sm font-medium text-slate-700">
          Dia
          <input
            type="date"
            {...register("date", { required: true })}
            className="rounded-xl border border-slate-200 px-3 py-2 text-sm shadow-sm focus:border-brand-400 focus:outline-none"
          />
        </label>

        <label className="flex flex-col gap-1 text-sm font-medium text-slate-700">
          Horário
          <input
            type="time"
            {...register("time", { required: true })}
            className="rounded-xl border border-slate-200 px-3 py-2 text-sm shadow-sm focus:border-brand-400 focus:outline-none"
          />
        </label>

        <button
          type="submit"
          className="md:col-span-2 inline-flex items-center justify-center gap-2 rounded-xl bg-brand-500 px-6 py-3 text-sm font-semibold text-white shadow-lg transition hover:bg-brand-600"
        >
          {t("book_session")}
        </button>
      </form>

      {status === "success" && (
        <div className="rounded-xl border border-emerald-200 bg-emerald-50 p-3 text-sm text-emerald-700">
          Sessão agendada com sucesso! Um lembrete será enviado antes da consulta.
        </div>
      )}
      {status === "error" && (
        <div className="rounded-xl border border-red-200 bg-red-50 p-3 text-sm text-red-700">
          Não foi possível comunicar com o servidor. Salvamos seu interesse e entraremos em contato.
        </div>
      )}
    </div>
  );
}
