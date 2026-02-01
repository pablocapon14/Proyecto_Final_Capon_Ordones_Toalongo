
clear; clc; close all;

%% LECTURA DE DATOS
datos = readtable("dron_datos_K5.csv");

t = datos.tiempo_s;     % Tiempo [s]
h = datos.altura_cm;    % Altura [cm]

%% =========================================================
%% PREPROCESAMIENTO
%% =========================================================

% Eliminar tiempos repetidos
[t, idx] = unique(t);
h = h(idx);

N = length(t);

% Derivada discreta
dh = diff(h);
dt = diff(t);
pendiente = dh ./ dt;   % tamaño N-1

%% =========================================================
%% DETECCION DE PUNTOS DINAMICOS
%% =========================================================

umbral = 1;   % cm/s (ajustable)

% Vector lógico del MISMO tamaño que t
idx_dinamicos = false(N,1);

% Siempre conservar primer y último punto
idx_dinamicos(1)   = true;
idx_dinamicos(end) = true;

% Asignar pendiente a puntos intermedios
idx_dinamicos(2:N) = abs(pendiente) > umbral;

% Filtrar
t_dyn = t(idx_dinamicos);
h_dyn = h(idx_dinamicos);

%% =========================================================
%% INTERPOLACION SOBRE ENVOLVENTE DINAMICA
%% =========================================================

t_interp = linspace(min(t_dyn), max(t_dyn), 10 * length(t_dyn))';
h_interp = interp1(t_dyn, h_dyn, t_interp, 'pchip');

%% =========================================================
%% GUARDAR DATOS INTERPOLADOS EN CSV
%% =========================================================

datos_interpolados = table( ...
    t_interp, ...
    h_interp, ...
    'VariableNames', { ...
        'tiempo_s', ...
        'altura_interp_cm' ...
    } ...
);

writetable(datos_interpolados, ...
    "datos_interpolados.csv");

disp("Archivo generado");

%% =========================================================
%% GRAFICA COMPARATIVA
%% =========================================================

figure;
plot(t, h, 'o', 'MarkerSize', 3); hold on;
plot(t_interp, h_interp, 'b', 'LineWidth', 2);
grid on;

xlabel('Tiempo [s]');
ylabel('Altura [cm]');
title('Altura vs tiempo (envolvente dinámica reconstruida)');

legend('Datos originales', 'Envolvente interpolada', 'Location','best');
