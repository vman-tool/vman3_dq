from vman_dq.cli import main


def test_cli_writes_report_to_requested_file(tmp_path):
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.md"
    input_file.write_text("id10104\n1\n")

    result = main([str(input_file), "-r", "-o", str(output_file)])

    assert result == 0
    assert output_file.is_file()
    assert output_file.read_text().startswith("# ")
    assert not (tmp_path / "reports" / "dqa_report.md").exists()
