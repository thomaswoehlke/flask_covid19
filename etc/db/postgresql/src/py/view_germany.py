create_view_germany = "" \
            + "CREATE VIEW "  \
            + "    view_who_germany "  \
            + "AS "  \
            + "SELECT DISTINCT "  \
            + "    date_reported, "  \
            + "    country_code, "  \
            + "    new_deaths, "  \
            + "    cumulative_deaths, "  \
            + "    new_cases, "  \
            + "    cumulative_cases, "  \
            + "    country "  \
            + "FROM "  \
            + "    who_global_data o "  \
            + "        LEFT JOIN "  \
            + "    who_date_reported wdr "  \
            + "    ON "  \
            + "            wdr.id = o.date_reported_id "  \
            + "        LEFT JOIN "  \
            + "    who_country wc "  \
            + "    ON "  \
            + "            wc.id = o.country_id "  \
            + "WHERE country_code = 'DE' "  \
            + "ORDER BY date_reported DESC " \
            + ""
