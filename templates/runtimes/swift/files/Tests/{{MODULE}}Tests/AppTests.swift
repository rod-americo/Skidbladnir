import Foundation
import XCTest
@testable import {{MODULE}}Core

final class AppTests: XCTestCase {
    func testEventPreservesTimestampAndStructuredFields() throws {
        let event = App.startupEvent(now: Date(timeIntervalSince1970: 0))
        XCTAssertEqual(event.ts, "1970-01-01T00:00:00Z")
        XCTAssertEqual(event.evt, "startup")
        XCTAssertEqual(event.lvl, "INFO")
        let data = try JSONEncoder().encode(event)
        let decoded = try JSONDecoder().decode(LogEvent.self, from: data)
        XCTAssertEqual(decoded.svc, {{PROJECT_NAME_LITERAL}})
        XCTAssertEqual(decoded.ts, event.ts)
    }
}
