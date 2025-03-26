import pytest

from dlms_cosem.hdlc import address, fields, frames
from dlms_cosem.hdlc.address import HdlcAddress
from dlms_cosem.io import HdlcTransport


def test_hdlc_frame_format_field_from_bytes():
    in_bytes = bytes.fromhex("a01d")
    f = fields.DlmsHdlcFrameFormatField.from_bytes(in_bytes)
    assert f.length == 29
    assert not f.segmented


def test_hdlc_frame_format_filed_from_bytes_segmented():
    in_bytes = bytes.fromhex("a81d")
    f = fields.DlmsHdlcFrameFormatField.from_bytes(in_bytes)
    assert f.length == 29
    assert f.segmented


def test_hdlc_frame_format_raises_value_error_too_long():
    with pytest.raises(ValueError):
        fields.DlmsHdlcFrameFormatField(length=999999, segmented=False)


def test_hdlc_frame_format_to_bytes_not_segmented():
    f = fields.DlmsHdlcFrameFormatField(length=29, segmented=False)
    assert f.to_bytes().hex() == "a01d"


def test_hdlc_frame_format_to_bytes_segmented():
    f = fields.DlmsHdlcFrameFormatField(length=29, segmented=True)
    assert f.to_bytes().hex() == "a81d"


class TestHdlcAddress:
    def test_find_address(self):
        frame = "7ea87e210396a4090f01160002020f02160002020f03160002020f04160002020f05160002020f0616000204120017110009060000160000ff0202010902030f0116010002030f0216010002030f0316010002030f0416010002030f0516010002030f0616010002030f0716010002030f0816010002030f09160100016ff37e"
        frame_bytes = bytes.fromhex(frame)
        (
            destination_address,
            source_address,
        ) = address.HdlcAddress.find_address_in_frame_bytes(frame_bytes)
        assert destination_address == (16, None, 1)
        assert source_address == (1, None, 1)

    @pytest.mark.parametrize(
        "hdlc_address,resulting_bytes",
        [
            ((1, None, "client"), b"\x03"),
            ((16, None, "client"), b"\x21"),
            ((0b1001010, None, "server"), b"\x95"),
            ((0b0100101, None, "client"), b"\x4b"),
            ((1, 17, "server"), b"\x02\x23"),
        ],
        # TODO: need to find references of multiy byte addresses to test.
    )
    def test_client_address_just_logical(self, hdlc_address, resulting_bytes):
        add = address.HdlcAddress(
            logical_address=hdlc_address[0],
            physical_address=hdlc_address[1],
            address_type=hdlc_address[2],
        )
        assert add.to_bytes() == resulting_bytes

    def test_find_4_byte_address(self):
        """
        Source address is using 4 bytes.
        :return:
        """
        frame1 = b"~\xa0#\x03\x00\x02\x00#s\xc0H\x81\x80\x14\x05\x02\x00\x80\x06\x02\x00\x80\x07\x04\x00\x00\x00\x01\x08\x04\x00\x00\x00\x01\xcej~"
        frame2 = b"~\xa0#!\x00\x02\x00#s\xf6\xc5\x81\x80\x14\x05\x02\x00\x80\x06\x02\x00\x80\x07\x04\x00\x00\x00\x01\x08\x04\x00\x00\x00\x01\xcej~"

        (
            destination_address,
            source_address,
        ) = address.HdlcAddress.find_address_in_frame_bytes(frame1)
        assert destination_address == (1, None, 1)
        assert source_address == (1, 17, 4)

        (
            destination_address,
            source_address,
        ) = address.HdlcAddress.find_address_in_frame_bytes(frame2)
        assert destination_address == (16, None, 1)
        assert source_address == (1, 17, 4)


class TestCrc:
    def test_crc(self):
        data = "033f"
        correct_crc = "5bec"

        _crc = frames.HCS
        result = _crc.calculate_for(bytes.fromhex(data))
        assert result == bytes.fromhex(correct_crc)


class TestHdlcFrameValidation:
    def test_frame_is_enclosed_by_hdlc_flag(self):
        data = b"\x7effff\x7e"
        assert frames.frame_is_enclosed_by_hdlc_flags(data)

    @pytest.mark.parametrize("data", [b"\x7effff", b"ffff\x7e", b"ffff"])
    def test_frame_is_enclosed_by_hdlc_flag_fail(self, data):
        assert not frames.frame_is_enclosed_by_hdlc_flags(data)


class TestSnrmFrame:
    def test_parses_correct(self):
        out_data = bytes.fromhex("7ea00802232193bd647e")
        destination_address = address.HdlcAddress(
            logical_address=1, physical_address=17, address_type="server"
        )

        # Public client
        source_address = address.HdlcAddress(
            logical_address=16, physical_address=None, address_type="client"
        )
        snrm = frames.SetNormalResponseModeFrame(destination_address, source_address)

        assert snrm.to_bytes() == out_data


class TestUAFrame:
    def test_parser_correctly(self):
        out_data = bytes.fromhex(
            "7EA01F21022373E6C781801205019A06019A070400000001080400000001CCA27E"
        )
        # from device so public client is destination address.
        source_address = address.HdlcAddress(
            logical_address=1, physical_address=17, address_type="server"
        )

        # Public client
        destination_address = address.HdlcAddress(
            logical_address=16, physical_address=None, address_type="client"
        )

        information = out_data[9:-3]
        ua = frames.UnNumberedAcknowledgmentFrame(
            destination_address, source_address, information
        )
        print(ua.hcs.hex())
        print(ua.to_bytes().hex())
        print(out_data.hex())
        assert ua.to_bytes() == out_data

    def test_from_bytes(self):
        in_data = b"~\xa0\x1f!\x02#s\xe6\xc7\x81\x80\x12\x05\x01\x9a\x06\x01\x9a\x07\x04\x00\x00\x00\x01\x08\x04\x00\x00\x00\x01\xcc\xa2~"
        frame = frames.UnNumberedAcknowledgmentFrame.from_bytes(in_data)
        assert in_data == frame.to_bytes()

    def test_4_byte_address(self):
        frame1 = b"~\xa0#\x03\x00\x02\x00#s\xc0H\x81\x80\x14\x05\x02\x00\x80\x06\x02\x00\x80\x07\x04\x00\x00\x00\x01\x08\x04\x00\x00\x00\x01\xcej~"
        frame2 = b"~\xa0#!\x00\x02\x00#s\xf6\xc5\x81\x80\x14\x05\x02\x00\x80\x06\x02\x00\x80\x07\x04\x00\x00\x00\x01\x08\x04\x00\x00\x00\x01\xcej~"

        frame = frames.UnNumberedAcknowledgmentFrame.from_bytes(frame1)
        assert frame1 == frame.to_bytes()

        frame = frames.UnNumberedAcknowledgmentFrame.from_bytes(frame2)
        assert frame2 == frame.to_bytes()


class TestInformationFrame:
    def test_construct(self):
        total = bytes.fromhex(
            "7EA02C02232110AF9FE6E600601DA109060760857405080101BE10040E01000000065F1F0400001E1DFFFFC5E47E"
        )
        information_part = bytes.fromhex(
            "E6E600601DA109060760857405080101BE10040E01000000065F1F0400001E1DFFFF"
        )
        server_address = address.HdlcAddress(
            logical_address=1, physical_address=17, address_type="server"
        )

        # Public client
        client_address = address.HdlcAddress(
            logical_address=16, physical_address=None, address_type="client"
        )
        frame = frames.InformationFrame(
            destination_address=server_address,
            source_address=client_address,
            payload=information_part,
            send_sequence_number=0,
            receive_sequence_number=0,
            segmented=False,
            final=True,
        )

        print(total)
        print(frame.to_bytes())
        assert frame.to_bytes() == total


class TestInformationResponseFrame:
    def test_contruct(self):
        total = bytes.fromhex(
            "7EA0382102233034E7E6E7006129A109060760857405080101A203020100A305A103020100BE10040E0800065F1F0400001E1D04C80007B86A7E"
        )
        information_part = bytes.fromhex(
            "E6E7006129A109060760857405080101A203020100A305A103020100BE10040E0800065F1F0400001E1D04C80007"
        )
        server_address = address.HdlcAddress(
            logical_address=1, physical_address=17, address_type="server"
        )

        # Public client
        client_address = address.HdlcAddress(
            logical_address=16, physical_address=None, address_type="client"
        )
        frame = frames.InformationFrame(
            destination_address=client_address,
            source_address=server_address,
            payload=information_part,
            send_sequence_number=0,
            receive_sequence_number=1,
            segmented=False,
            final=True,
        )

        print(f"length = {frame.frame_length}  :: {len(frame.to_bytes())}")

        print(total.hex())
        print(frame.to_bytes().hex())
        assert frame.to_bytes() == total

    def test_rebuild_frame(self):
        in_data = b"~\xa08!\x02#04\xe7\xe6\xe7\x00a)\xa1\t\x06\x07`\x85t\x05\x08\x01\x01\xa2\x03\x02\x01\x00\xa3\x05\xa1\x03\x02\x01\x00\xbe\x10\x04\x0e\x08\x00\x06_\x1f\x04\x00\x00\x1e\x1d\x04\xc8\x00\x07\xb8j~"
        info = frames.InformationFrame.from_bytes(in_data)
        print(info)
        assert info.to_bytes().hex() == in_data.hex()


class TestInformationControlField:
    def test_from_bytes(self):
        in_byte = bytes.fromhex("30")
        ctrl = fields.InformationControlField.from_bytes(in_byte)
        assert ctrl.receive_sequence_number == 1
        assert ctrl.send_sequence_number == 0
        assert ctrl.final


class TestUnnumberedInformationFrame:
    def test_parse(self):
        data = b"~\xa2CA\x08\x83\x13\x85\xeb\xe6\xe7\x00\x0f@\x00\x00\x00\x00\x01\x1b\x02\x02\t\x06\x00\x00\x01\x00\x00\xff\t\x0c\x07\xe3\x0c\x10\x01\x07;(\xff\x80\x00\xff\x02\x03\t\x06\x01\x00\x01\x07\x00\xff\x06\x00\x00\x04b\x02\x02\x0f\x00\x16\x1b\x02\x03\t\x06\x01\x00\x02\x07\x00\xff\x06\x00\x00\x00\x00\x02\x02\x0f\x00\x16\x1b\x02\x03\t\x06\x01\x00\x03\x07\x00\xff\x06\x00\x00\x05\xe3\x02\x02\x0f\x00\x16\x1d\x02\x03\t\x06\x01\x00\x04\x07\x00\xff\x06\x00\x00\x00\x00\x02\x02\x0f\x00\x16\x1d\x02\x03\t\x06\x01\x00\x1f\x07\x00\xff\x10\x00\x00\x02\x02\x0f\xff\x16!\x02\x03\t\x06\x01\x003\x07\x00\xff\x10\x00K\x02\x02\x0f\xff\x16!\x02\x03\t\x06\x01\x00G\x07\x00\xff\x10\x00\x00\x02\x02\x0f\xff\x16!\x02\x03\t\x06\x01\x00 \x07\x00\xff\x12\t\x03\x02\x02\x0f\xff\x16#\x02\x03\t\x06\x01\x004\x07\x00\xff\x12\t\xc3\x02\x02\x0f\xff\x16#\x02\x03\t\x06\x01\x00H\x07\x00\xff\x12\t\x04\x02\x02\x0f\xff\x16#\x02\x03\t\x06\x01\x00\x15\x07\x00\xff\x06\x00\x00\x00\x00\x02\x02\x0f\x00\x16\x1b\x02\x03\t\x06\x01\x00\x16\x07\x00\xff\x06\x00\x00\x00\x00\x02\x02\x0f\x00\x16\x1b\x02\x03\t\x06\x01\x00\x17\x07\x00\xff\x06\x00\x00\x00\x00\x02\x02\x0f\x00\x16\x1d\x02\x03\t\x06\x01\x00\x18\x07\x00\xff\x06\x00\x00\x00\x00\x02\x02\x0f\x00\x16\x1d\x02\x03\t\x06\x01\x00)\x07\x00\xff\x06\x00\x00\x04b\x02\x02\x0f\x00\x16\x1b\x02\x03\t\x06\x01\x00*\x07\x00\xff\x06\x00\x00\x00\x00\x02\x02\x0f\x00\x16\x1b\x02\x03\t\x06\x01\x00+\x07\x00\xff\x06\x00\x00\x05\xe2\x02\x02\x0f\x00\x16\x1d\x02\x03\t\x06\x01\x00,\x07\x00\xff\x06\x00\x00\x00\x00\x02\x02\x0f\x00\x16\x1d\x02\x03\t\x06\x01\x00=\x07\x00\xff\x06\x00\x00\x00\x00\x02\x02\x0f\x00\x16\x1b\x02\x03\t\x06\x01\x00>\x07\x00\xff\x06\x00\x00\x00\x00\x02\x02\x0f\x00\x16\x1b\x02\x03\t\x06\x01\x00?\x07\x00\xff\x06\x00\x00\x00\x00\x02\x02\x0f\x00\x16\x1d\x02\x03\t\x06\x01\x00@\x07\x00\xff\x06\x00\x00\x00\x00\x02\x02\x0f\x00\x16\x1d\x02\x03\t\x06\x01\x00\x01\x08\x00\xff\x06\x00\x99Y\x86\x02\x02\x0f\x00\x16\x1e\x02\x03\t\x06\x01\x00\x02\x08\x00\xff\x06\x00\x00\x00\x08\x02\x02\x0f\x00\x16\x1e\x02\x03\t\x06\x01\x00\x03\x08\x00\xff\x06\x00d\xedK\x02\x02\x0f\x00\x16 \x02\x03\t\x06\x01\x00\x04\x08\x00\xff\x06\x00\x00\x00\x05\x02\x02\x0f\x00\x16 \xbe@~"
        ui = frames.UnnumberedInformationFrame.from_bytes(data)
        assert ui.to_bytes() == data


class TestUnnumberedInformationControlField:
    def test_parse(self):
        data = b"\x13"
        cf = fields.UnnumberedInformationControlField.from_bytes(data)
        assert cf.to_bytes() == data


class TestFiorentiniLocal:
    """ no physical address when talking to fiorentini meters"""

    def test_frame(self):
        response = b'~\xa0\x07!\x03s\x01@~'

        frame = frames.UnNumberedAcknowledgmentFrame.from_bytes(response)

    def test_ua_frame(self):
        frame = frames.UnNumberedAcknowledgmentFrame(
            destination_address=HdlcAddress(logical_address=16, physical_address=None, address_type='client',
                                            extended_addressing=False),
            source_address=HdlcAddress(logical_address=1, physical_address=None, address_type='server',
                                       extended_addressing=False), payload=b'', segmented=False, final=True)

        fsc = frame.fcs
    def test_fcs(self):
        data = b'~\xa0\x07!\x03s\x01@~'
        fcs = data[-3:-1]
        assert fcs == b"\x01@"
        # frame_content should be everything except flag and fcs


# class TestKaifaMeter:
#
#     def test_kaifa_data(self):
#         # data = "7ea09b01000110561be6e7000f40000000090c07e7090401103400ff800000021209074b464d5f30303109103733343031353730313132353335343409084d41333034483444060000044f0600000000060000000006000000c0060000088f06000005aa060000057c06000008da06000008f906000008e6090c07e7090401103400ff8000000608c141c9060000000006001ae03806013151959d787e"
#         data = "7ea11d01000110b0aee6e7000f4000000000022409060100000281ff09074b464d5f30303109060000600100ff09103733343031353730333037383433393509060000600107ff09074d41333034483409060100010700ff060000017209060100020700ff060000000009060100030700ff060000000009060100040700ff0600000050090601001f0700ff06000001be09060100330700ff060000047b09060100470700ff060000009409060100200700ff06000008ee09060100340700ff06000008e609060100480700ff06000008dd09060000010000ff090c07e709040111132dffffc40009060100010800ff0600bc0d9009060100020800ff060000000009060100030800ff06001c05dc09060100040800ff06000fed42acfd7e"
#         frame = frames.UnnumberedInformationFrame.from_bytes(bytes.fromhex(data))
#         print(frame)
