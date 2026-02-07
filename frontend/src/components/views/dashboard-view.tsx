'use client';

import { useMemo } from "react";
import { useQuery } from "@tanstack/react-query";
import dayjs from "dayjs";
import { useTranslation } from "react-i18next";
import { Line } from "react-chartjs-2";
import { ensureChartRegistration } from "@/lib/chart";
import { CalendarDays, ChartLine, Users } from "lucide-react";
import { getAppointments, getOverview, getPatients } from "@/services/api";

ensureChartRegistration();

export function DashboardView() {
  const { t } = useTranslation();
  const { data: appointments = [] } = useQuery({
    queryKey: ["appointments"],
    queryFn: getAppointments,
  });
  const { data: overview } = useQuery({
    queryKey: ["overview"],
    queryFn: getOverview,
  });
  const { data: patients = [] } = useQuery({
    queryKey: ["patients"],
    queryFn: getPatients,
  });

  const chartData = useMemo(() => {
    const grouped = appointments.reduce<Record<string, number>>((acc, appointment) => {
      const day = dayjs(appointment.start_time).format("DD/MM");
      acc[day] = (acc[day] ?? 0) + 1;
      return acc;
    }, {});
    const labels = Object.keys(grouped).length
      ? Object.keys(grouped)
      : Array.from({ length: 5 }).map((_, index) =>
          dayjs().add(index, "day").format("DD/MM"),
        );
    const values = labels.map((label) => grouped[label] ?? Math.round(Math.random() * 3));
    return {
      labels,
      datasets: [
        {
          label: "Agendamentos",
          data: values,
          borderColor: "#FF478B",
          backgroundColor: "rgba(255, 71, 139, 0.15)",
          tension: 0.4,
          fill: true,
        },
      ],
    };
  }, [appointments]);

  const upcoming = useMemo(
    () =>
      appointments
        .filter((item) => dayjs(item.start_time).isAfter(dayjs()))
        .slice(0, 5),
    [appointments],
  );

  return (
    <div className="space-y-8">
      <div className="grid gap-6 md:grid-cols-3">
        <div className="card">
          <div className="flex items-center justify-between">
            <p className="text-sm font-medium text-slate-500">{t("appointments")}</p>
            <CalendarDays className="h-5 w-5 text-brand-500" />
          </div>
          <p className="mt-2 text-3xl font-bold">{overview?.total_appointments ?? upcoming.length}</p>
          <p className="mt-1 text-xs text-slate-500">
            {upcoming.length} agendamentos futuros
          </p>
        </div>
        <div className="card">
          <div className="flex items-center justify-between">
            <p className="text-sm font-medium text-slate-500">{t("revenue")}</p>
            <ChartLine className="h-5 w-5 text-brand-500" />
          </div>
          <p className="mt-2 text-3xl font-bold">
            R${" "}
            {(overview?.total_revenue ?? 0).toLocaleString("pt-BR", {
              minimumFractionDigits: 2,
            })}
          </p>
          <p className="mt-1 text-xs text-slate-500">
            {overview?.paid_invoices ?? 0} faturas pagas
          </p>
        </div>
        <div className="card">
          <div className="flex items-center justify-between">
            <p className="text-sm font-medium text-slate-500">{t("patients")}</p>
            <Users className="h-5 w-5 text-brand-500" />
          </div>
          <p className="mt-2 text-3xl font-bold">{patients.length}</p>
          <p className="mt-1 text-xs text-slate-500">Pacientes ativos registrados</p>
        </div>
      </div>

      <div className="card">
        <h2 className="section-title mb-4">Fluxo de agendamentos</h2>
        <Line data={chartData} options={{ responsive: true, plugins: { legend: { display: false } } }} />
      </div>

      <div className="card">
        <h2 className="section-title mb-4">Próximos atendimentos</h2>
        <ul className="space-y-3">
          {upcoming.map((appointment) => (
            <li
              key={appointment.id}
              className="flex items-center justify-between rounded-xl border border-slate-200 px-4 py-3"
            >
              <div>
                <p className="font-semibold">{appointment.service_name}</p>
                <p className="text-sm text-slate-500">
                  {dayjs(appointment.start_time).format("DD/MM/YYYY HH:mm")}
                </p>
              </div>
              <span className="rounded-full bg-brand-100 px-3 py-1 text-xs font-medium text-brand-600">
                {appointment.status}
              </span>
            </li>
          ))}
          {!upcoming.length && (
            <p className="text-sm text-slate-500">
              Nenhum agendamento futuro encontrado. Experimente criar um novo pelo Portal do Paciente.
            </p>
          )}
        </ul>
      </div>
    </div>
  );
}
